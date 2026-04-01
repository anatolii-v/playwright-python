import logging
import uuid
from pathlib import Path

import pytest
from faker import Faker
from pytest import Item
from playwright.sync_api import (
    APIRequestContext,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

# Re-export shared user fixtures for UI suite.
from fixtures.users import existing_user, new_user  # noqa: F401
from pages.home_page import HomePage

REPORTS_DIR = Path("reports")
TRACES_DIR = REPORTS_DIR / "traces"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
BASE_API_URL = "https://automationexercise.com/api"
faker = Faker()

TRACES_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call):
    """Expose setup/call/teardown results on request.node."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """
    Capture screenshot for failed UI tests only.
    The fixture safely skips API tests that do not use Playwright page fixture.
    """
    yield
    if not hasattr(request.node, "rep_call") or not request.node.rep_call.failed:
        return
    if "page" not in request.fixturenames:
        return

    try:
        page = request.getfixturevalue("page")
    except AssertionError:
        # The page fixture may already be torn down for some failure paths.
        return
    test_name = request.node.name
    screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
    logging.info(f"Saving the screenshot to {screenshot_path}")
    page.screenshot(path=screenshot_path, full_page=True)


@pytest.fixture
def home_page(page: Page):
    page.add_init_script(
        """
        () => {
            setInterval(() => {
                document.querySelectorAll(
                    '.fc-dialog-overlay, .fc-consent-root, #ez-cookie-dialog-wrapper'
                ).forEach((el) => el.remove());
            }, 500);
        }
        """
    )
    try:
        home = HomePage(page).open()
    except PlaywrightTimeoutError:
        # Retry once to reduce external-site transient failures.
        home = HomePage(page).open()
    home.accept_cookies_if_present()
    yield home


@pytest.fixture
def ensure_logged_in_user(home_page, created_account, new_user):
    # Primary path: API-created user makes UI auth independent and fast.
    login_page = home_page.go_to_login_or_signup()
    logged_home = login_page.login(
        {"email": created_account["email"], "password": created_account["password"]}
    )
    if logged_home.page.get_by_text("Logged in as").count() > 0:
        return logged_home

    # Fallback path for rare API/UI propagation timing issues.
    signup_page = home_page.go_to_login_or_signup()
    signup_page.start_signup(new_user)
    signup_page.fill_account_details(new_user)
    signup_page.page.get_by_role("button", name="Create Account").click()
    signup_page.page.get_by_role("link", name="Continue").click()
    return HomePage(signup_page.page)


@pytest.fixture
def api_base_url():
    return BASE_API_URL


@pytest.fixture
def api_context(playwright, api_base_url) -> APIRequestContext:
    context = playwright.request.new_context(base_url=f"{api_base_url}/")
    yield context
    context.dispose()


@pytest.fixture
def account_payload_factory():
    def _make_payload(**overrides):
        unique_email = f"api_{uuid.uuid4().hex}@test.com"
        payload = {
            "name": faker.name(),
            "email": unique_email,
            "password": "Password123!",
            "title": "Mr",
            "birth_date": "1",
            "birth_month": "1",
            "birth_year": "1990",
            "firstname": "Api",
            "lastname": "User",
            "company": "ACME",
            "address1": "Street 1",
            "address2": "Street 2",
            "country": "United States",
            "zipcode": "10001",
            "state": "NY",
            "city": "New York",
            "mobile_number": "1234567890",
        }
        payload.update(overrides)
        return payload

    return _make_payload


@pytest.fixture
def created_account(api_context, account_payload_factory):
    payload = account_payload_factory()
    response = api_context.post("createAccount", form=payload, timeout=20_000)
    assert response.status == 200
    assert response.json().get("responseCode") == 201

    yield payload

    response = api_context.delete(
        "deleteAccount",
        form={"email": payload["email"], "password": payload["password"]},
        timeout=20_000,
    )
    if response.status != 200:
        logging.warning("Cleanup deleteAccount request failed for %s", payload["email"])
