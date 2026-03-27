import logging
from playwright.sync_api import Page, Dialog, expect

logger = logging.getLogger(__name__)


class ContactUsPage:

    NAME_INPUT = {"role": "textbox", "name": "Name"}
    EMAIL_INPUT = {"role": "textbox", "name": "Email"}
    SUBJECT_INPUT = {"role": "textbox", "name": "Subject"}
    MESSAGE_INPUT = {"role": "textbox", "name": "Your Message Here"}
    CHOOSE_FILE_BUTTON = {"role": "button", "name": "Choose File"}
    SUBMIT_BUTTON = {"role": "button", "name": "Submit"}

    def __init__(self, page: Page):
        self.page = page

    def fill_contact_form(self, user: dict):
        logger.info("Filling contact form")
        self.page.get_by_role(**self.NAME_INPUT).fill(user["name"])
        self.page.get_by_role(**self.EMAIL_INPUT).first.fill(user["email"])
        self.page.get_by_role(**self.SUBJECT_INPUT).fill("Test subject")
        self.page.get_by_role(**self.MESSAGE_INPUT).fill("Test message")

    def attach_file(self, file):
        logger.info("Attaching test file")
        self.page.get_by_role(**self.CHOOSE_FILE_BUTTON).set_input_files(file)

    def submit_message(self):
        logger.info("Submitting the message")
        def accept_alert(alert: Dialog) -> None:
            logger.info("Accepting the alert")
            assert alert.type == 'confirm'
            alert.accept()

        self.page.on('dialog', accept_alert)
        self.page.get_by_role(**self.SUBMIT_BUTTON).click()

    def assert_success_message(self, text):
        logger.info(f"Checking that the text '{text}' is visible")
        expect(self.page.locator("#contact-page")).to_contain_text(text)
