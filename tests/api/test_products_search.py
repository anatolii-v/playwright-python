import pytest


def _extract_names(products):
    return [item.get("name", "").lower() for item in products]


@pytest.mark.api
@pytest.mark.parametrize("keyword", ["top", "jean"])
def test_search_product_valid_keywords(api_context, keyword):
    response = api_context.post(
        "searchProduct",
        form={"search_product": keyword},
        timeout=20_000,
    )
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200
    assert len(body["products"]) > 0


@pytest.mark.api
def test_search_product_case_insensitive(api_context):
    lower = api_context.post(
        "searchProduct",
        form={"search_product": "top"},
        timeout=20_000,
    ).json()
    upper = api_context.post(
        "searchProduct",
        form={"search_product": "TOP"},
        timeout=20_000,
    ).json()
    assert lower["responseCode"] == 200
    assert upper["responseCode"] == 200
    assert len(lower["products"]) == len(upper["products"])


@pytest.mark.api
def test_search_product_partial_keyword_match(api_context):
    response = api_context.post(
        "searchProduct",
        form={"search_product": "je"},
        timeout=20_000,
    )
    body = response.json()
    assert body["responseCode"] == 200
    assert len(body["products"]) > 0


@pytest.mark.api
def test_search_product_results_include_keyword(api_context):
    keyword = "top"
    response = api_context.post(
        "searchProduct",
        form={"search_product": keyword},
        timeout=20_000,
    )
    names = _extract_names(response.json()["products"])
    assert any(keyword in name for name in names)


@pytest.mark.api
@pytest.mark.parametrize(
    "payload, expected_code",
    [
        ({"search_product": ""}, 200),
        ({}, 400),
    ],
)
def test_search_product_empty_or_missing_param(api_context, payload, expected_code):
    response = api_context.post("searchProduct", form=payload, timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == expected_code


@pytest.mark.api
def test_search_product_non_existent_keyword_returns_empty(api_context):
    response = api_context.post(
        "searchProduct",
        form={"search_product": "xyzxyzxyz"},
        timeout=20_000,
    )
    body = response.json()
    assert body["responseCode"] == 200
    assert body["products"] == []


@pytest.mark.api
def test_search_product_special_characters_no_crash(api_context):
    response = api_context.post(
        "searchProduct",
        form={"search_product": "!@#$%^&*()"},
        timeout=20_000,
    )
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 200


@pytest.mark.api
@pytest.mark.parametrize("method", ["get", "delete"])
def test_search_product_method_validation(api_context, method):
    response = getattr(api_context, method)("searchProduct", timeout=20_000)
    body = response.json()
    assert response.status == 200
    assert body["responseCode"] == 405
