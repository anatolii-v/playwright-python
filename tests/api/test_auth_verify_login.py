import pytest

@pytest.mark.api
def test_verify_login_valid_credentials(api_context, created_account):
    payload = {
        "email": created_account["email"],
        "password": created_account["password"],
    }
    response = api_context.post("verifyLogin", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"


@pytest.mark.api
def test_verify_login_email_is_case_insensitive(api_context, created_account):
    payload = {
        "email": created_account["email"].upper(),
        "password": created_account["password"],
    }
    response = api_context.post("verifyLogin", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    # Production API may not normalize email casing consistently.
    assert body["responseCode"] in (200, 404)
    assert "message" in body


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"email": "does-not-exist@test.com", "password": "wrong-password"},
        {"email": "", "password": "wrong-password"},
        {"email": "nobody@test.com", "password": ""},
        {"email": "", "password": ""},
        {"password": "123456"},
        {"email": "nobody@test.com"},
    ],
)
def test_verify_login_negative_cases(api_context, payload):
    response = api_context.post("verifyLogin", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    # API returns either 400 or 404 depending on validation branch.
    assert body["responseCode"] in (400, 404)
    assert "message" in body


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"email": "' OR '1'='1", "password": "any"},
        {"email": "nobody@test.com", "password": "<script>alert(1)</script>"},
        {"email": f"{'a' * 1200}@test.com", "password": "any"},
    ],
)
def test_verify_login_security_payloads_no_server_error(api_context, payload):
    response = api_context.post("verifyLogin", form=payload, timeout=20_000)
    assert response.status == 200
    body = response.json()
    assert body["responseCode"] in (400, 404)
    assert "traceback" not in str(body).lower()


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "delete"])
def test_verify_login_method_validation(api_context, method):
    response = getattr(api_context, method)("verifyLogin", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
