import pytest
import requests


@pytest.mark.api
def test_flow_create_verify_get_detail_delete(api_base_url, account_payload_factory):
    payload = account_payload_factory()

    create = requests.post(f"{api_base_url}/createAccount", data=payload, timeout=20).json()
    assert create["responseCode"] == 201

    verify = requests.post(
        f"{api_base_url}/verifyLogin",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    ).json()
    assert verify["responseCode"] == 200

    details = requests.get(
        f"{api_base_url}/getUserDetailByEmail",
        params={"email": payload["email"]},
        timeout=20,
    ).json()
    assert details["responseCode"] == 200
    assert details["user"]["email"] == payload["email"]

    delete = requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    ).json()
    assert delete["responseCode"] == 200


@pytest.mark.api
def test_flow_create_update_verify_delete(api_base_url, account_payload_factory):
    payload = account_payload_factory()
    requests.post(f"{api_base_url}/createAccount", data=payload, timeout=20)

    updated_name = "Updated Name By Flow"
    update = requests.put(
        f"{api_base_url}/updateAccount",
        data={**payload, "name": updated_name},
        timeout=20,
    ).json()
    assert update["responseCode"] == 200

    verify = requests.post(
        f"{api_base_url}/verifyLogin",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    ).json()
    assert verify["responseCode"] == 200

    requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    )


@pytest.mark.api
def test_flow_products_to_search_consistency(api_base_url):
    products = requests.get(f"{api_base_url}/productsList", timeout=20).json()["products"]
    assert len(products) > 0

    first_name = products[0]["name"]
    first_token = first_name.split()[0]
    search = requests.post(
        f"{api_base_url}/searchProduct",
        data={"search_product": first_token},
        timeout=20,
    ).json()
    names = [item["name"] for item in search["products"]]
    assert any(first_name.lower() == name.lower() for name in names)


@pytest.mark.api
def test_flow_delete_account_then_verify_login_not_found(api_base_url, account_payload_factory):
    payload = account_payload_factory()
    requests.post(f"{api_base_url}/createAccount", data=payload, timeout=20)
    requests.delete(
        f"{api_base_url}/deleteAccount",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    )

    verify = requests.post(
        f"{api_base_url}/verifyLogin",
        data={"email": payload["email"], "password": payload["password"]},
        timeout=20,
    ).json()
    assert verify["responseCode"] == 404
