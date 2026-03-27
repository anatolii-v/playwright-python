import pytest
import requests


@pytest.mark.api
def test_delete_account_valid_credentials(api_base_url, created_account):
    response = requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": created_account["email"], "password": created_account["password"]},
        timeout=20,
    )
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert body["message"] == "Account deleted!"


@pytest.mark.api
def test_delete_account_then_verify_login_user_not_found(api_base_url, created_account):
    requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": created_account["email"], "password": created_account["password"]},
        timeout=20,
    )
    verify = requests.post(
        f"{api_base_url}/verifyLogin",
        data={"email": created_account["email"], "password": created_account["password"]},
        timeout=20,
    )
    verify_body = verify.json()
    assert verify.status_code == 200
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
def test_delete_account_negative_cases(api_base_url, payload, expected_code):
    response = requests.delete(f"{api_base_url}/deleteAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == expected_code


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "post"])
def test_delete_account_method_validation(api_base_url, method):
    response = getattr(requests, method)(f"{api_base_url}/deleteAccount", timeout=20)
    assert response.status_code == 405
