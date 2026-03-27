import pytest
import requests


@pytest.mark.api
def test_get_user_detail_valid_email_returns_user_object(api_base_url, created_account):
    response = requests.get(
        f"{api_base_url}/getUserDetailByEmail",
        params={"email": created_account["email"]},
        timeout=20,
    )
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert "user" in body


@pytest.mark.api
def test_get_user_detail_required_fields_and_no_password(api_base_url, created_account):
    response = requests.get(
        f"{api_base_url}/getUserDetailByEmail",
        params={"email": created_account["email"]},
        timeout=20,
    )
    user = response.json()["user"]
    assert "id" in user
    assert "name" in user
    assert "email" in user
    assert "password" not in user


@pytest.mark.api
@pytest.mark.parametrize(
    "params, expected_code",
    [
        ({"email": "missing_123@test.com"}, 404),
        ({"email": ""}, (200, 400, 404)),
        ({}, 400),
        ({"email": "invalid-email"}, (200, 400, 404)),
    ],
)
def test_get_user_detail_negative_cases(api_base_url, params, expected_code):
    response = requests.get(f"{api_base_url}/getUserDetailByEmail", params=params, timeout=20)
    body = response.json()
    assert response.status_code == 200
    if isinstance(expected_code, tuple):
        assert body["responseCode"] in expected_code
    else:
        assert body["responseCode"] == expected_code


@pytest.mark.api
def test_get_user_detail_security_sql_injection_input(api_base_url):
    response = requests.get(
        f"{api_base_url}/getUserDetailByEmail",
        params={"email": "' OR '1'='1"},
        timeout=20,
    )
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] in (400, 404)
    assert "traceback" not in str(body).lower()


@pytest.mark.api
def test_get_user_detail_response_headers_no_sensitive_data(api_base_url, created_account):
    response = requests.get(
        f"{api_base_url}/getUserDetailByEmail",
        params={"email": created_account["email"]},
        timeout=20,
    )
    headers_text = " ".join(f"{k}:{v}" for k, v in response.headers.items()).lower()
    assert "x-api-key" not in headers_text
    assert "authorization" not in headers_text


@pytest.mark.api
@pytest.mark.parametrize("method", ["post", "delete"])
def test_get_user_detail_method_validation(api_base_url, method):
    response = getattr(requests, method)(f"{api_base_url}/getUserDetailByEmail", timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 405
