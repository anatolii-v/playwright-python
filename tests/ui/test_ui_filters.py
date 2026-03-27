import re

import pytest
from playwright.sync_api import expect

BASE_SITE = "https://automationexercise.com"


def _strip_ad_interstitial(page):
    """Drop URL fragments on /products (e.g. #google_vignette from ads on CI runners)."""
    base = page.url.split("#", 1)[0].rstrip("/")
    if base.endswith("/products") and "#" in page.url:
        page.goto(f"{BASE_SITE}/products", wait_until="domcontentloaded", timeout=60000)
    page.evaluate(
        """
        () => {
            document.querySelectorAll('.fc-dialog-overlay, .fc-consent-root')
              .forEach((el) => el.remove());
        }
        """
    )


def _open_listing(page, path: str):
    """Navigate with a stable path (UI uses these same routes)."""
    page.goto(f"{BASE_SITE}{path}", wait_until="domcontentloaded", timeout=60000)


@pytest.mark.ui
def test_tc_015_filter_products_by_women_category(home_page):
    home_page.go_to_products_page()
    page = home_page.page
    _strip_ad_interstitial(page)
    _open_listing(page, "/category_products/1")
    expect(page.get_by_text("Women - Dress Products")).to_be_visible()
    assert "category_products" in page.url


@pytest.mark.ui
def test_tc_016_filter_products_by_men_category(home_page):
    home_page.go_to_products_page()
    page = home_page.page
    _strip_ad_interstitial(page)
    _open_listing(page, "/category_products/6")
    expect(page.get_by_text("Men - Jeans Products")).to_be_visible()
    assert "category_products" in page.url


@pytest.mark.ui
def test_tc_017_filter_products_by_brand(home_page):
    home_page.go_to_products_page()
    page = home_page.page
    _strip_ad_interstitial(page)
    _open_listing(page, "/brand_products/Polo")
    page.wait_for_url("**/brand_products/**", timeout=60000)
    expect(page.get_by_text("Brand - Polo Products")).to_be_visible()
    assert "brand_products" in page.url
    expect(page.locator(".features_items .product-image-wrapper").first).to_be_visible()


@pytest.mark.ui
def test_tc_018_switch_between_brands(home_page):
    home_page.go_to_products_page()
    page = home_page.page
    _strip_ad_interstitial(page)
    _open_listing(page, "/brand_products/Polo")
    expect(page.locator("h2.title")).to_contain_text("Polo")
    _open_listing(page, "/brand_products/H%26M")
    expect(page.locator("h2.title")).to_contain_text(re.compile(r"H\s*&\s*M"))
