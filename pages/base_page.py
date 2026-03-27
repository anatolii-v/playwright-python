from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
import logging

logger = logging.getLogger(__name__)

class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def check_header_text(self, expected_text):
        logger.info(f"Checking that header contains {expected_text}")
        expect(self.page.locator("h2.title")).to_contain_text(expected_text)

    def dismiss_consent_overlays(self):
        # Remove overlays that intercept pointer events in the demo site.
        self.page.evaluate(
            """
            () => {
                document.querySelectorAll(
                    '.fc-dialog-overlay, .fc-consent-root, #ez-cookie-dialog-wrapper'
                ).forEach((el) => el.remove());
            }
            """
        )

    def safe_click(self, locator):
        try:
            locator.click()
        except PlaywrightTimeoutError:
            self.dismiss_consent_overlays()
            locator.click(force=True)

    def safe_hover(self, locator):
        try:
            locator.hover()
        except PlaywrightTimeoutError:
            self.dismiss_consent_overlays()
            locator.hover(force=True)
