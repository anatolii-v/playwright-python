import pytest
import requests


@pytest.mark.api
def test_brands_list_returns_200_and_not_empty(api_base_url):
    response = requests.get(f"{api_base_url}/brandsList", timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body.get("brands"), list)
    assert len(body["brands"]) > 0


@pytest.mark.api
def test_brands_list_schema_has_id_and_name(api_base_url):
    response = requests.get(f"{api_base_url}/brandsList", timeout=20)
    brands = response.json()["brands"]
    for brand in brands:
        assert "id" in brand
        assert "brand" in brand


@pytest.mark.api
def test_brands_list_response_time_under_2_seconds(api_base_url):
    response = requests.get(f"{api_base_url}/brandsList", timeout=20)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2


@pytest.mark.api
@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_brands_list_method_validation(api_base_url, method):
    response = getattr(requests, method)(f"{api_base_url}/brandsList", timeout=20)
    body = response.json()
    assert response.status_code == 200
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
