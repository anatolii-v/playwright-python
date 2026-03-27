import pytest
import requests


@pytest.mark.api
def test_create_account_valid_required_fields(api_base_url, account_payload_factory):
    payload = account_payload_factory()
    response = requests.post(f"{api_base_url}/createAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 201
    assert body["message"] == "User created!"

    requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    )


@pytest.mark.api
def test_create_account_duplicate_email(api_base_url, created_account):
    response = requests.post(f"{api_base_url}/createAccount", data=created_account, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 400
    assert "already exists" in body["message"].lower()


@pytest.mark.api
@pytest.mark.parametrize(
    "override, expected_message_fragment",
    [
        ({"name": None}, "name"),
        ({"email": None}, "email"),
        ({"password": None}, "password"),
        ({"email": "invalid-email"}, None),
    ],
)
def test_create_account_negative_validation(
    api_base_url, account_payload_factory, override, expected_message_fragment
):
    payload = account_payload_factory()
    for key, value in override.items():
        if value is None:
            payload.pop(key, None)
        else:
            payload[key] = value

    response = requests.post(f"{api_base_url}/createAccount", data=payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 400
    message = body["message"].lower()
    if expected_message_fragment is not None:
        assert expected_message_fragment.lower() in message or "bad request" in message
    else:
        assert len(message) > 0


@pytest.mark.api
def test_create_account_empty_body(api_base_url):
    response = requests.post(f"{api_base_url}/createAccount", timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 400
    assert "bad request" in body["message"].lower()


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"name": "' OR '1'='1"},
        {"name": "<script>alert(1)</script>"},
        {"password": "x" * 600},
    ],
)
def test_create_account_security_payloads(api_base_url, account_payload_factory, payload):
    request_payload = account_payload_factory(**payload)
    response = requests.post(f"{api_base_url}/createAccount", data=request_payload, timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] in (201, 400)
    assert "traceback" not in str(body).lower()

    if body["responseCode"] == 201:
        requests.delete(
            f"{api_base_url}/deleteAccount",
            data={"email": request_payload["email"], "password": request_payload["password"]},
            timeout=20,
        )


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "delete"])
def test_create_account_method_validation(api_base_url, method):
    response = getattr(requests, method)(f"{api_base_url}/createAccount", timeout=20)
    assert response.status_code == 405
