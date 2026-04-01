import pytest


@pytest.mark.api
def test_update_account_valid_name_change(api_context, created_account):
    payload = {**created_account, "name": "Updated API User"}
    response = api_context.put("updateAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"


@pytest.mark.api
def test_update_account_multiple_fields(api_context, created_account):
    payload = {**created_account, "name": "Updated User", "city": "LA", "state": "CA"}
    response = api_context.put("updateAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"


@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_code",
    [
        ({"name": "A", "email": "john_12345@test.com", "password": "wrong"}, 404),
        ({"name": "A", "email": "missing_999@test.com", "password": "123456"}, 404),
        ({"email": "john_12345@test.com", "password": "123456"}, (200, 400, 404)),
        ({"name": "A", "email": "john_12345@test.com"}, 400),
    ],
)
def test_update_account_negative_cases(api_context, payload, expected_code):
    response = api_context.put("updateAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    if isinstance(expected_code, tuple):
        assert body["responseCode"] in expected_code
    else:
        assert body["responseCode"] == expected_code


@pytest.mark.api
@pytest.mark.parametrize("name_payload", ["<script>alert(1)</script>", "' OR '1'='1"])
def test_update_account_security_name_payload(api_context, created_account, name_payload):
    payload = {**created_account, "name": name_payload}
    response = api_context.put("updateAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert "traceback" not in str(body).lower()


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "post"])
def test_update_account_method_validation(api_context, method):
    response = getattr(api_context, method)("updateAccount", timeout=20_000)
    assert response.status == 405
