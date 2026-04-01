import pytest


@pytest.mark.api
def test_delete_account_valid_credentials(api_context, created_account):
    response = api_context.delete(
        "deleteAccount",
        form={"email": created_account["email"], "password": created_account["password"]},
        timeout=20_000,
    )
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert body["message"] == "Account deleted!"


@pytest.mark.api
def test_delete_account_then_verify_login_user_not_found(api_context, created_account):
    api_context.delete(
        "deleteAccount",
        form={"email": created_account["email"], "password": created_account["password"]},
        timeout=20_000,
    )
    verify = api_context.post(
        "verifyLogin",
        form={"email": created_account["email"], "password": created_account["password"]},
        timeout=20_000,
    )
    verify_body = verify.json()
    assert verify.status == 200
    assert verify_body["responseCode"] == 404
    assert "not found" in verify_body["message"].lower()


@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_code",
    [
        ({"email": "john_12345@test.com", "password": "bad"}, 404),
        ({"email": "nobody_12345@test.com", "password": "bad"}, 404),
        ({"email": "", "password": "bad"}, 404),
        ({"email": "john_12345@test.com", "password": ""}, 404),
        ({}, 400),
    ],
)
def test_delete_account_negative_cases(api_context, payload, expected_code):
    response = api_context.delete("deleteAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == expected_code


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "post"])
def test_delete_account_method_validation(api_context, method):
    response = getattr(api_context, method)("deleteAccount", timeout=20_000)
    assert response.status == 405
