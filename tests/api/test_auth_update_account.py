import pytest
import requests


@pytest.mark.api
def test_update_account_valid_name_change(api_base_url, created_account):
    payload = {**created_account, "name": "Updated API User"}
    response = requests.put(f"{api_base_url}/updateAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"


@pytest.mark.api
def test_update_account_multiple_fields(api_base_url, created_account):
    payload = {**created_account, "name": "Updated User", "city": "LA", "state": "CA"}
    response = requests.put(f"{api_base_url}/updateAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
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
def test_update_account_negative_cases(api_base_url, payload, expected_code):
    response = requests.put(f"{api_base_url}/updateAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    if isinstance(expected_code, tuple):
        assert body["responseCode"] in expected_code
    else:
        assert body["responseCode"] == expected_code


@pytest.mark.api
@pytest.mark.parametrize("name_payload", ["<script>alert(1)</script>", "' OR '1'='1"])
def test_update_account_security_name_payload(api_base_url, created_account, name_payload):
    payload = {**created_account, "name": name_payload}
    response = requests.put(f"{api_base_url}/updateAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert "traceback" not in str(body).lower()


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "post"])
def test_update_account_method_validation(api_base_url, method):
    response = getattr(requests, method)(f"{api_base_url}/updateAccount", timeout=20)
    assert response.status_code == 405
