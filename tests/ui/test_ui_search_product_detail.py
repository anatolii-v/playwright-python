import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_tc_011_search_for_existing_product(home_page):
    products = home_page.go_to_products_page()
    products.search_product("top")
    products.check_header_text("Searched Products")
    cards = products.page.locator(".features_items .productinfo p")
    expect(cards.first).to_be_visible()
    names = [cards.nth(i).inner_text().lower() for i in range(min(cards.count(), 8))]
    assert any("top" in name for name in names)


@pytest.mark.ui
def test_tc_012_search_for_non_existent_product(home_page):
    products = home_page.go_to_products_page()
    products.search_product("xyznotexist123")
    products.check_header_text("Searched Products")
    expect(products.page.locator(".features_items .product-image-wrapper")).to_have_count(0)
    expect(products.page.get_by_role("textbox", name="Search Product")).to_be_visible()


@pytest.mark.ui
def test_tc_013_view_product_detail_page(home_page):
    product_page = home_page.go_to_products_page().go_to_first_product_details()
    product_page.check_visibility_of_product_details()
    expect(product_page.page.locator("button.cart")).to_be_visible()


@pytest.mark.ui
def test_tc_014_add_product_to_cart_from_detail_page(home_page):
    product_page = home_page.go_to_products_page().go_to_first_product_details()
    product_page.page.locator("input#quantity").fill("3")
    product_page.add_to_cart()
    cart_page = product_page.view_cart()
    # Ensure cart table has loaded before validating counts.
    expect(cart_page.page.locator("#cart_info_table tbody tr").first).to_be_visible()
    cart_page.check_number_of_items_in_cart(1)
    cart_page.check_product_quantity(3)
