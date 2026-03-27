import logging
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

class SubscriptionMixin:
    ENTER_EMAIL_FOR_SUBSCRIPTION_FIELD = "#susbscribe_email"
    SUBSCRIBE_BUTTON = "#subscribe"

    def subscribe(self):
        logger.info("Filling up subscription email")
        subscribe_field = self.page.locator(self.ENTER_EMAIL_FOR_SUBSCRIPTION_FIELD)
        subscribe_field.scroll_into_view_if_needed()
        subscribe_field.fill("john_doe@test.com")
        self.page.locator(self.SUBSCRIBE_BUTTON).click()

    def check_that_subscribed_successfully(self):
        logger.info("Checking that subscription is successful")
        expect(self.page.get_by_text("You have been successfully")).to_be_visible()
