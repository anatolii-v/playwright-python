import logging
from pages.base_page import BasePage
from mixins.subscription_mixin import SubscriptionMixin
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

class CartPage(BasePage, SubscriptionMixin):

    CART_TABLE = "#cart_info_table"
    PRODUCT = "tbody tr"
    QUANTITY_INPUT = "input.cart_quantity_input"
    DELETE_PRODUCT_BUTTON = ".cart_quantity_delete"

    def check_card_is_empty(self):
        logger.info("Checking the card is empty")
        expect(self.page.get_by_text("Cart is empty!")).to_be_visible()

    def check_number_of_items_in_cart(self, expected_number):
        logger.info(f"Checking number of items in cart is {expected_number}")
        table = self.page.locator(self.CART_TABLE)
        actual_number_of_items = table.locator(self.PRODUCT).count()
        assert actual_number_of_items == expected_number, \
            f"The actual number of items is {actual_number_of_items}"

    def check_product_quantity(self, expected_quantity, product_line=1):
        logger.info(f"Checking product quantity is {expected_quantity}")
        quantity_input = self.page.locator(f"#product-{product_line} .cart_quantity button")
        expect(quantity_input).to_have_text(str(expected_quantity))

    def delete_product(self):
        logger.info("Deleting product from cart")
        self.safe_click(self.page.locator(self.DELETE_PRODUCT_BUTTON))
