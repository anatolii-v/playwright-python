import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_tc_026_verify_all_main_navigation_links(home_page):
    page = home_page.page
    nav_checks = [
        ("Home", "https://automationexercise.com/"),
        ("Products", "products"),
        ("Cart", "view_cart"),
        ("Signup / Login", "login"),
        ("Test Cases", "test_cases"),
        ("API Testing", "api_list"),
        ("Contact us", "contact_us"),
    ]

    for link_name, expected_url_part in nav_checks:
        page.get_by_role("link", name=link_name).first.click()
        assert expected_url_part in page.url

    page.get_by_role("link", name="Video Tutorials").click()
    assert "youtube" in page.url.lower() or "automationexercise.com/video_tutorials" in page.url.lower()


@pytest.mark.ui
def test_tc_027_verify_footer_links_and_content(home_page):
    page = home_page.page
    footer = page.locator("footer")
    footer.scroll_into_view_if_needed()
    expect(page.get_by_text("Subscription")).to_be_visible()
    social_links = page.locator("a[href*='facebook'], a[href*='twitter'], a[href*='youtube']")
    assert social_links.count() >= 1

    footer_links = footer.locator("a")
    for i in range(min(footer_links.count(), 5)):
        href = footer_links.nth(i).get_attribute("href")
        if href and href.startswith("/"):
            page.goto(f"https://automationexercise.com{href}")
            expect(page).not_to_have_url(lambda url: "404" in url)
            expect(page.get_by_text("Subscription")).to_be_visible()
