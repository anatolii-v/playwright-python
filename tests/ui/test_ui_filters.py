import pytest
from playwright.sync_api import expect


def _dismiss_overlay(page):
    page.evaluate(
        """
        () => {
            document.querySelectorAll('.fc-dialog-overlay, .fc-consent-root')
              .forEach((el) => el.remove());
        }
        """
    )


def _select_category(page, parent_href: str, child_href: str):
    _dismiss_overlay(page)
    parent = page.locator(f"a[href='{parent_href}']").first
    expect(parent).to_be_visible(timeout=10000)
    parent.click()
    child = page.locator(f"a[href='{child_href}']:visible").first
    expect(child).to_be_visible(timeout=10000)
    child.click()
    page.wait_for_url("**/category_products/**", timeout=60000)


@pytest.mark.ui
def test_tc_015_filter_products_by_women_category(home_page):
    products = home_page.go_to_products_page()
    _select_category(products.page, "#Women", "/category_products/1")
    expect(products.page.get_by_text("Women - Dress Products")).to_be_visible()
    assert "category_products" in products.page.url


@pytest.mark.ui
def test_tc_016_filter_products_by_men_category(home_page):
    products = home_page.go_to_products_page()
    _select_category(products.page, "#Men", "/category_products/6")
    expect(products.page.get_by_text("Men - Jeans Products")).to_be_visible()
    assert "category_products" in products.page.url


@pytest.mark.ui
def test_tc_017_filter_products_by_brand(home_page):
    products = home_page.go_to_products_page()
    brand_link = products.page.locator(".brands-name a[href*='Polo']:visible").first
    _dismiss_overlay(products.page)
    expect(brand_link).to_be_visible(timeout=10000)
    brand_link.click()
    products.page.wait_for_url("**/brand_products/**", timeout=60000)
    expect(products.page.get_by_text("Brand - Polo Products")).to_be_visible()
    assert "brand_products" in products.page.url
    expect(products.page.locator(".features_items .product-image-wrapper").first).to_be_visible()


@pytest.mark.ui
def test_tc_018_switch_between_brands(home_page):
    products = home_page.go_to_products_page()
    _dismiss_overlay(products.page)
    polo = products.page.locator(".brands-name a[href*='Polo']:visible").first
    expect(polo).to_be_visible(timeout=10000)
    polo.click()
    products.page.wait_for_url("**/brand_products/**", timeout=60000)
    expect(products.page.get_by_text("Brand - Polo Products")).to_be_visible()
    _dismiss_overlay(products.page)
    hm = products.page.locator(".brands-name a[href*='H&M']:visible").first
    expect(hm).to_be_visible(timeout=10000)
    hm.click()
    products.page.wait_for_url("**/brand_products/**", timeout=60000)
    expect(products.page.get_by_text("Brand - H&M Products")).to_be_visible()
