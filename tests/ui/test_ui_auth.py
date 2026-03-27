import pytest
from playwright.sync_api import expect


def _complete_signup(signup_page, user):
    signup_page.start_signup(user)
    signup_page.fill_account_details(user)
    signup_page.page.evaluate(
        """
        () => {
            document.querySelectorAll('.fc-dialog-overlay, .fc-consent-root')
              .forEach((el) => el.remove());
        }
        """
    )
    signup_page.page.get_by_role("button", name="Create Account").click(force=True)
    expect(signup_page.page.get_by_text("Account Created!")).to_be_visible()
    return signup_page.continue_after_creation()


@pytest.mark.ui
def test_tc_001_successful_login(ensure_logged_in_user):
    home = ensure_logged_in_user
    expect(home.page.get_by_text("Logged in as")).to_be_visible()
    expect(home.page.get_by_role("link", name="Signup / Login")).not_to_be_visible()


@pytest.mark.ui
def test_tc_002_login_with_invalid_credentials(home_page):
    login_page = home_page.go_to_login_or_signup()
    login_page.login({"email": "wrong_user@test.com", "password": "wrong-pass"})
    login_page.assert_authentication_error("Your email or password is incorrect!")
    expect(login_page.page).to_have_url("https://automationexercise.com/login")


@pytest.mark.ui
def test_tc_003_successful_registration(home_page, new_user):
    signup_page = home_page.go_to_login_or_signup()
    home = _complete_signup(signup_page, new_user)
    home.assert_logged_in(new_user["name"])
    home.delete_account()
    home.assert_account_is_deleted()


@pytest.mark.ui
def test_tc_004_logout(ensure_logged_in_user):
    home = ensure_logged_in_user
    back_to_login = home.logout()
    back_to_login.check_that_logged_out()
    expect(back_to_login.page.get_by_role("link", name="Signup / Login")).to_be_visible()


@pytest.mark.ui
def test_tc_005_register_with_existing_email(home_page, new_user):
    # Ensure this email exists first, then validate duplicate signup behavior.
    signup_page = home_page.go_to_login_or_signup()
    logged_home = _complete_signup(signup_page, new_user)
    signup_page = logged_home.logout()
    signup_page.start_signup({"name": "Any Name", "email": new_user["email"]})
    expect(signup_page.page.locator("#form")).to_contain_text("already exist")
    assert "/signup" in signup_page.page.url or "/login" in signup_page.page.url
