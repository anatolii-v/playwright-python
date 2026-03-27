import logging
from playwright.sync_api import Error as PlaywrightError, expect

from pages.base_page import BasePage
from pages.login_or_signup_page import LoginOrSignupPage
from pages.contact_us_page import ContactUsPage
from pages.test_cases_page import TestCasesPage
from pages.products_page import ProductsPage
from mixins.subscription_mixin import SubscriptionMixin
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)

class HomePage(BasePage, SubscriptionMixin):

    UAT_URL = "https://automationexercise.com/"
    COOKIE_BUTTON = {"role": "button", "name": "Consent"}
    SIGNUP_LINK = {"role": "link", "name": " Signup / Login"}
    LOGOUT_LINK = {"role": "link", "name": " Logout"}
    CONTACT_US = {"role": "link", "name": " Contact us"}
    DELETE_ACCOUNT_LINK = {"role": "link", "name": " Delete Account"}
    TEST_CASES_LINK = {"role": "link", "name": " Test Cases"}
    PRODUCTS_LINK = {"role": "link", "name": " Products"}
    CART_BUTTON = {"selector": "li a[href*='cart']"}

    def open(self):
        logger.info("Opening home page")
        try:
            self.page.goto(self.UAT_URL, wait_until="domcontentloaded", timeout=60000)
        except PlaywrightError as exc:
            if "ERR_NAME_NOT_RESOLVED" not in str(exc):
                raise
            logger.warning("Retrying home page open after DNS resolution failure")
            self.page.wait_for_timeout(1500)
            self.page.goto(self.UAT_URL, wait_until="domcontentloaded", timeout=60000)
        return self

    def accept_cookies_if_present(self):
        # Cookie widget can render with different button labels; handle common variants.
        candidates = [
            self.page.get_by_role("button", name="Consent"),
            self.page.get_by_role("button", name="Accept All"),
            self.page.get_by_role("button", name="I Agree"),
            self.page.locator("button.fc-cta-consent"),
        ]
        for btn in candidates:
            if btn.count() > 0 and btn.first.is_visible():
                logger.info("Accepting cookies")
                btn.first.click()
                break
        self.dismiss_consent_overlays()

    def go_to_login_or_signup(self):
        logger.info("Navigating to Signup/Login")
        self.accept_cookies_if_present()
        self.safe_click(self.page.get_by_role(**self.SIGNUP_LINK))
        return LoginOrSignupPage(self.page)

    def assert_logged_in(self, name: str):
        logger.info(f"Checking that the user {name} is logged in")
        expect(self.page.get_by_text(f"Logged in as {name}")).to_be_visible()

    def delete_account(self):
        logger.info("Deleting account")
        self.safe_click(self.page.get_by_role(**self.DELETE_ACCOUNT_LINK))

    def assert_account_is_deleted(self):
        logger.info("Checking that account is deleted")
        expect(self.page.get_by_text("Account Deleted!")).to_be_visible()

    def logout(self):
        logger.info("Logging out")
        self.safe_click(self.page.get_by_role(**self.LOGOUT_LINK))
        return LoginOrSignupPage(self.page)
    
    def go_to_contact_us_page(self):
        logger.info("Navigating to Contact Us")
        self.safe_click(self.page.get_by_role(**self.CONTACT_US))
        return ContactUsPage(self.page)
    
    def go_to_test_cases_page(self):
        logger.info("Navigating to Test Cases")
        self.safe_click(self.page.get_by_role(**self.TEST_CASES_LINK))
        return TestCasesPage(self.page)
    
    def go_to_products_page(self):
        logger.info("Navigating to Products page")
        products_url = f"{self.UAT_URL.rstrip('/')}/products"
        self.safe_click(self.page.get_by_role(**self.PRODUCTS_LINK))
        self.page.wait_for_url("**/products", timeout=60000)
        # Any hash (#google_vignette, etc.) breaks the products sidebar; common on GitHub-hosted runners.
        base_products = self.page.url.split("#", 1)[0].rstrip("/")
        if base_products.endswith("/products") and "#" in self.page.url:
            logger.info("Reloading products page to drop URL fragment")
            self.page.goto(products_url, wait_until="domcontentloaded", timeout=60000)
        return ProductsPage(self.page)
    
    def go_to_cart(self):
        logger.info("Open cart")
        self.safe_click(self.page.locator(**self.CART_BUTTON))
        return CartPage(self.page)
