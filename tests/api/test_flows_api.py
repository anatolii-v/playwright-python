import pytest


@pytest.mark.api
def test_flow_create_verify_get_detail_delete(api_context, account_payload_factory):
    payload = account_payload_factory()

    create = api_context.post("createAccount", form=payload, timeout=20_000).json()
    assert create["responseCode"] == 201

    verify = api_context.post(
        "verifyLogin",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    ).json()
    assert verify["responseCode"] == 200

    details = api_context.get(
        "getUserDetailByEmail",
        params={"email": payload["email"]},
        timeout=20_000,
    ).json()
    assert details["responseCode"] == 200
    assert details["user"]["email"] == payload["email"]

    delete = api_context.delete(
        "deleteAccount",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    ).json()
    assert delete["responseCode"] == 200


@pytest.mark.api
def test_flow_create_update_verify_delete(api_context, account_payload_factory):
    payload = account_payload_factory()
    api_context.post("createAccount", form=payload, timeout=20_000)

    updated_name = "Updated Name By Flow"
    update = api_context.put(
        "updateAccount",
        form={**payload, "name": updated_name},
        timeout=20_000,
    ).json()
    assert update["responseCode"] == 200

    verify = api_context.post(
        "verifyLogin",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    ).json()
    assert verify["responseCode"] == 200

    api_context.delete(
        "deleteAccount",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    )


@pytest.mark.api
def test_flow_products_to_search_consistency(api_context):
    products = api_context.get("productsList", timeout=20_000).json()["products"]
    assert len(products) > 0

    first_name = products[0]["name"]
    first_token = first_name.split()[0]
    search = api_context.post(
        "searchProduct",
        form={"search_product": first_token},
        timeout=20_000,
    ).json()
    names = [item["name"] for item in search["products"]]
    assert any(first_name.lower() == name.lower() for name in names)


@pytest.mark.api
def test_flow_delete_account_then_verify_login_not_found(api_context, account_payload_factory):
    payload = account_payload_factory()
    api_context.post("createAccount", form=payload, timeout=20_000)
    api_context.delete(
        "deleteAccount",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    )

    verify = api_context.post(
        "verifyLogin",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    ).json()
    assert verify["responseCode"] == 404
