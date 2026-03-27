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


def _complete_signup(signup_page, user):
    signup_page.start_signup(user)
    signup_page.fill_account_details(user)
    _dismiss_overlay(signup_page.page)
    signup_page.page.get_by_role("button", name="Create Account").click(force=True)
    expect(signup_page.page.get_by_text("Account Created!")).to_be_visible()
    return signup_page.continue_after_creation()


def _add_first_product(home_page):
    products = home_page.go_to_products_page()
    products.add_first_product()
    products.page.get_by_role("link", name="View Cart").click()
    return products.page


@pytest.mark.ui
def test_tc_006_add_single_product_to_cart(home_page):
    page = _add_first_product(home_page)
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(1)
    expect(page.locator(".cart_description a").first).to_be_visible()
    expect(page.locator(".cart_price p").first).to_be_visible()
    expect(page.locator(".cart_quantity button").first).to_have_text("1")


@pytest.mark.ui
def test_tc_007_add_multiple_products_to_cart(home_page):
    products = home_page.go_to_products_page()
    products.add_first_product()
    products.continue_shoping()
    products.add_second_product()
    cart_page = products.open_cart()
    cart_page.check_number_of_items_in_cart(2)
    expect(cart_page.page.locator(".cart_description a")).to_have_count(2)


@pytest.mark.ui
def test_tc_008_remove_product_from_cart(home_page):
    page = _add_first_product(home_page)
    page.locator(".cart_quantity_delete").first.click()
    expect(page.get_by_text("Cart is empty!")).to_be_visible()


@pytest.mark.ui
def test_tc_009_checkout_as_logged_in_user(ensure_logged_in_user):
    page = _add_first_product(ensure_logged_in_user)
    _dismiss_overlay(page)
    page.get_by_text("Proceed To Checkout").click(force=True)
    expect(page.get_by_text("Address Details")).to_be_visible()
    expect(page.get_by_text("Review Your Order")).to_be_visible()
    page.locator("textarea[name='message']").fill("Please deliver after 6 PM")
    _dismiss_overlay(page)
    page.get_by_role("link", name="Place Order").click(force=True)
    page.locator("input[name='name_on_card']").fill("John Doe")
    page.locator("input[name='card_number']").fill("4111111111111111")
    page.locator("input[name='cvc']").fill("123")
    page.locator("input[name='expiry_month']").fill("12")
    page.locator("input[name='expiry_year']").fill("2030")
    _dismiss_overlay(page)
    page.get_by_role("button", name="Pay and Confirm Order").click(force=True)
    expect(page.get_by_text("Order Placed!")).to_be_visible()


@pytest.mark.ui
def test_tc_010_checkout_as_guest_then_register(home_page, new_user):
    page = _add_first_product(home_page)
    _dismiss_overlay(page)
    page.get_by_text("Proceed To Checkout").click(force=True)
    _dismiss_overlay(page)
    page.get_by_role("link", name="Register / Login").click(force=True)

    home = _complete_signup(home_page.go_to_login_or_signup(), new_user)
    cart_page = home.go_to_cart()
    _dismiss_overlay(cart_page.page)
    cart_page.page.get_by_text("Proceed To Checkout").click(force=True)
    cart_page.page.locator("textarea[name='message']").fill("Guest to user flow")
    _dismiss_overlay(cart_page.page)
    cart_page.page.get_by_role("link", name="Place Order").click(force=True)
    cart_page.page.locator("input[name='name_on_card']").fill("John Doe")
    cart_page.page.locator("input[name='card_number']").fill("4111111111111111")
    cart_page.page.locator("input[name='cvc']").fill("123")
    cart_page.page.locator("input[name='expiry_month']").fill("12")
    cart_page.page.locator("input[name='expiry_year']").fill("2030")
    _dismiss_overlay(cart_page.page)
    cart_page.page.get_by_role("button", name="Pay and Confirm Order").click(force=True)
    expect(cart_page.page.get_by_text("Order Placed!")).to_be_visible()
