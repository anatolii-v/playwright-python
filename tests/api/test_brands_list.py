import time

import pytest


@pytest.mark.api
def test_brands_list_returns_200_and_not_empty(api_context):
    response = api_context.get("brandsList", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert isinstance(body.get("brands"), list)
    assert len(body["brands"]) > 0


@pytest.mark.api
def test_brands_list_schema_has_id_and_name(api_context):
    response = api_context.get("brandsList", timeout=20_000)
    brands = response.json()["brands"]
    for brand in brands:
        assert "id" in brand
        assert "brand" in brand


@pytest.mark.api
def test_brands_list_response_time_under_2_seconds(api_context):
    start = time.perf_counter()
    response = api_context.get("brandsList", timeout=20_000)
    elapsed_seconds = time.perf_counter() - start
    assert response.status == 200
    assert elapsed_seconds < 2


@pytest.mark.api
@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_brands_list_method_validation(api_context, method):
    response = getattr(api_context, method)("brandsList", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
