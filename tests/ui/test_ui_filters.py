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


@pytest.mark.ui
def test_tc_015_filter_products_by_women_category(home_page):
    products = home_page.go_to_products_page()
    _dismiss_overlay(products.page)
    products.page.locator("a[href='#Women']").click(force=True)
    _dismiss_overlay(products.page)
    products.page.locator("a[href='/category_products/1']").click(force=True)
    expect(products.page.get_by_text("Women - Dress Products")).to_be_visible()
    assert "category_products" in products.page.url


@pytest.mark.ui
def test_tc_016_filter_products_by_men_category(home_page):
    products = home_page.go_to_products_page()
    _dismiss_overlay(products.page)
    products.page.locator("a[href='#Men']").click(force=True)
    _dismiss_overlay(products.page)
    products.page.locator("a[href='/category_products/6']").click(force=True)
    expect(products.page.get_by_text("Men - Jeans Products")).to_be_visible()
    assert "category_products" in products.page.url


@pytest.mark.ui
def test_tc_017_filter_products_by_brand(home_page):
    products = home_page.go_to_products_page()
    brand_link = products.page.locator(".brands-name a[href*='Polo']")
    _dismiss_overlay(products.page)
    brand_link.click(force=True)
    expect(products.page.get_by_text("Brand - Polo Products")).to_be_visible()
    assert "brand_products" in products.page.url
    expect(products.page.locator(".features_items .product-image-wrapper").first).to_be_visible()


@pytest.mark.ui
def test_tc_018_switch_between_brands(home_page):
    products = home_page.go_to_products_page()
    _dismiss_overlay(products.page)
    products.page.get_by_role("link", name="Polo").click(force=True)
    expect(products.page.get_by_text("Brand - Polo Products")).to_be_visible()
    _dismiss_overlay(products.page)
    products.page.get_by_role("link", name="H&M").click(force=True)
    expect(products.page.get_by_text("Brand - H&M Products")).to_be_visible()
