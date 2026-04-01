import pytest


@pytest.mark.api
def test_create_account_valid_required_fields(api_context, account_payload_factory):
    payload = account_payload_factory()
    response = api_context.post("createAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 201
    assert body["message"] == "User created!"

    api_context.delete(
        "deleteAccount",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    )


@pytest.mark.api
def test_create_account_duplicate_email(api_context, created_account):
    response = api_context.post("createAccount", form=created_account, timeout=20_000)
    body = response.json()
    assert response.status == 200
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
    api_context, account_payload_factory, override, expected_message_fragment
):
    payload = account_payload_factory()
    for key, value in override.items():
        if value is None:
            payload.pop(key, None)
        else:
            payload[key] = value

    response = api_context.post("createAccount", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 400
    message = body["message"].lower()
    if expected_message_fragment is not None:
        assert expected_message_fragment.lower() in message or "bad request" in message
    else:
        assert len(message) > 0


@pytest.mark.api
def test_create_account_empty_body(api_context):
    response = api_context.post("createAccount", timeout=20_000)
    body = response.json()
    assert response.status == 200
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
def test_create_account_security_payloads(api_context, account_payload_factory, payload):
    request_payload = account_payload_factory(**payload)
    response = api_context.post("createAccount", form=request_payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] in (201, 400)
    assert "traceback" not in str(body).lower()

    if body["responseCode"] == 201:
        api_context.delete(
            "deleteAccount",
            form={"email": request_payload["email"], "password": request_payload["password"]},
            timeout=20_000,
        )


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "delete"])
def test_create_account_method_validation(api_context, method):
    response = getattr(api_context, method)("createAccount", timeout=20_000)
    assert response.status == 405
