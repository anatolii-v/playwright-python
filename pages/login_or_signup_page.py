import logging
from urllib.parse import urlencode, parse_qs
from playwright.sync_api import Page, Route, expect

logger = logging.getLogger(__name__)

class LoginOrSignupPage:

    NAME_INPUT = {"role": "textbox", "name": "Name"}
    EMAIL_INPUT = {"text": "Email Address"}
    PASSWORD_INPUT = {"role": "textbox", "name": "Password"}
    LOGIN_BUTTON = {"role": "button", "name": "Login"}
    SIGNUP_BUTTON = {"role": "button", "name": "Signup"}
    TITLE_MR_RADIO = {"role": "radio", "name": "Mr."}
    SIGNUP_PASSWORD_INPUT = {"role": "textbox", "name": "Password *"}
    NEWSLETTER_CHECKBOX = {"role": "checkbox", "name": "Sign up for our newsletter!"}
    SPECIAL_OFFERS_CHECKBOX = {"role": "checkbox", "name": "Receive special offers from"}
    FIRST_NAME_INPUT = {"role": "textbox", "name": "First name *"}
    LAST_NAME_INPUT = {"role": "textbox", "name": "Last name *"}
    ADDRESS_INPUT = {"role": "textbox", "name": "Address * (Street address, P."}
    COUNTRY_SELECT = {"text": "Country *"}
    STATE_INPUT = {"role": "textbox", "name": "State *"}
    CITY_INPUT = {"role": "textbox", "name": "City * Zipcode *"}
    ZIPCODE_INPUT = {"selector": "#zipcode"}
    MOBILE_INPUT = {"role": "textbox", "name": "Mobile Number *"}
    CREATE_ACCOUNT_BUTTON = {"role": "button", "name": "Create Account"}
    CONTINUE_LINK = {"role": "link", "name": "Continue"}


    def __init__(self, page: Page):
        self.page = page

    def login(self, user: dict):
        logger.info("Starting login")
        login_form = self.page.locator("form").filter(has_text="Login")
        login_form.get_by_placeholder(**self.EMAIL_INPUT).fill(user["email"])
        login_form.get_by_role(**self.PASSWORD_INPUT).fill(user["password"])
        self.page.get_by_role(**self.LOGIN_BUTTON).click()

        from pages.home_page import HomePage
        return HomePage(self.page)
    
    def login_via_wrong_password(self, user: dict):

        def intercept_login_request(route: Route):
            request = route.request
            if route.request.method != "POST" or not request.post_data:
                route.continue_()
                return
            logger.info("Injecting wrong password into login POST request")
            parsed = parse_qs(request.post_data, keep_blank_values=True)
            if "password" in parsed:
                parsed["password"] = ["wrongpassword"]
            else:
                logger.warning("Password field not found in POST data")
            route.continue_(post_data=urlencode(parsed, doseq=True))

        self.page.route("**/login", intercept_login_request, times=1)
        logger.info("Starting login")
        login_form = self.page.locator("form").filter(has_text="Login")
        login_form.get_by_placeholder(**self.EMAIL_INPUT).fill(user["email"])
        login_form.get_by_role(**self.PASSWORD_INPUT).fill(user["password"])
        self.page.get_by_role(**self.LOGIN_BUTTON).click()

    def fill_new_user_name(self, name: str):
        logger.info(f"Entering Username {name}")
        self.page.get_by_role(**self.NAME_INPUT).fill(name)

    def click_signup_button(self):
        logger.info("Clicking signup button")
        self.page.get_by_role(**self.SIGNUP_BUTTON).click()
        
    def start_signup(self, user: dict):
        logger.info("Starting signup")
        self.fill_new_user_name(user["name"])
        self.page.locator("form").filter(has_text="Signup") \
            .get_by_placeholder(**self.EMAIL_INPUT).fill(user["email"])
        self.page.get_by_role(**self.SIGNUP_BUTTON).click()

    def fill_account_details(self, user: dict):
        logger.info("Filling account details")
        self.page.get_by_role(**self.TITLE_MR_RADIO).check()
        self.page.get_by_role(**self.SIGNUP_PASSWORD_INPUT).fill(user["password"])
        self.page.get_by_role(**self.NEWSLETTER_CHECKBOX).check()
        self.page.get_by_role(**self.SPECIAL_OFFERS_CHECKBOX).check()
        self.page.locator("#days").select_option(user["date_of_birth"][0])
        self.page.locator("#months").select_option(user["date_of_birth"][1])
        self.page.locator("#years").select_option(user["date_of_birth"][2])
        self.page.get_by_role(**self.FIRST_NAME_INPUT).fill(user["first_name"])
        self.page.get_by_role(**self.LAST_NAME_INPUT).fill(user["last_name"])
        self.page.get_by_role(**self.ADDRESS_INPUT).fill(user["address"])
        self.page.get_by_label(**self.COUNTRY_SELECT).select_option(user["country"])
        self.page.get_by_role(**self.STATE_INPUT).fill(user["state"])
        self.page.get_by_role(**self.CITY_INPUT).fill(user["city"])
        self.page.locator(**self.ZIPCODE_INPUT).fill(user["zip"])
        self.page.get_by_role(**self.MOBILE_INPUT).fill(user["mobile"])

    def enter_invalid_email(self, invalid_email: str):
        logger.info(f"Entering invalid email: {invalid_email}")
        self.page.locator("form").filter(has_text="Signup") \
            .get_by_placeholder("Email Address").fill(invalid_email)

    def create_account(self):
        logger.info("Creating account")
        self.click_signup_button()
        expect(self.page.get_by_text("Account Created!")).to_be_visible()

    def continue_after_creation(self):
        self.page.get_by_role(**self.CONTINUE_LINK).click()

        from pages.home_page import HomePage
        return HomePage(self.page)
    
    def assert_authentication_error(self, text):
        logger.info(f"Checking that the text '{text}' is visible")
        expect(self.page.locator("#form")).to_contain_text(text)

    def check_that_logged_out(self):
        logger.info("Checking that user is logged out")
        expect(self.page.get_by_role(**self.LOGIN_BUTTON)).to_be_visible()

    def assert_validation_popup(self, expected_message: str, trigger_action=None):
        """
        Asserts that a browser-native validation popup appears with the expected message.
        If trigger_action is provided, it will be called to trigger the popup (e.g., clicking Signup).
        Otherwise, the method will click the Signup button by default.
        """
        dialog_message = None
        def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            dialog.dismiss()
        self.page.once("dialog", handle_dialog)
        if trigger_action:
            trigger_action()
        else:
            self.click_signup_button()
        assert dialog_message is not None, "No validation popup appeared."
        assert expected_message in dialog_message, f"Expected '{expected_message}' in popup, got '{dialog_message}'"

    def assert_email_validation_message(self, expected_message: str):
        """
        Asserts the browser-native validationMessage of the email input field.
        """
        logger.info(f"Checking that validation message contains {expected_message}")
        # Find the email input in the Signup form
        email_input = self.page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address")
        # Get the validation message
        actual_message = email_input.evaluate("el => el.validationMessage")
        assert expected_message in actual_message, f"Expected validation message to contain '{expected_message}', got '{actual_message}'"
