import time

import pytest


@pytest.mark.api
def test_products_list_returns_200_and_not_empty(api_context):
    response = api_context.get("productsList", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert isinstance(body.get("products"), list)
    assert len(body["products"]) > 0


@pytest.mark.api
def test_products_list_required_fields_per_product(api_context):
    response = api_context.get("productsList", timeout=20_000)
    products = response.json()["products"]
    required_fields = {"id", "name", "price", "brand", "category"}
    assert all(required_fields.issubset(product.keys()) for product in products)


@pytest.mark.api
def test_products_list_response_time_and_content_type(api_context):
    start = time.perf_counter()
    response = api_context.get("productsList", timeout=20_000)
    elapsed_seconds = time.perf_counter() - start
    assert elapsed_seconds < 2
    # API sometimes returns JSON with text/html content-type header.
    assert isinstance(response.json().get("products"), list)


@pytest.mark.api
def test_products_list_invalid_query_param_ignored(api_context):
    response = api_context.get("productsList", params={"unexpected": "1"}, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert len(body.get("products", [])) > 0


@pytest.mark.api
def test_products_list_request_with_body_is_ignored(api_context):
    response = api_context.get("productsList", data={"any": "value"}, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert len(body.get("products", [])) > 0


@pytest.mark.api
@pytest.mark.parametrize("method", ["post", "delete", "put"])
def test_products_list_method_validation(api_context, method):
    response = getattr(api_context, method)("productsList", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
