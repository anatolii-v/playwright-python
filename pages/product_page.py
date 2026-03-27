import logging
from playwright.sync_api import Page, expect
from pages.cart_page import CartPage
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ProductPage(BasePage):
    
    PRODUCT_INFORMATION_CONTAINER = 'div.product-information'
    QUANTITY_INPUT = "input#quantity"
    ADD_TO_CART_BUTTON = "button[type='button'].cart"
    VIEW_CART_LINK = ".modal-content a[href='/view_cart']"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_visibility_of_product_details(self):
        logging.info("Check product detail fields")
        expected_fields= "Category", "Availability", "Condition", "Brand"
        product_information_container = self.page.locator(self.PRODUCT_INFORMATION_CONTAINER)
        expect(product_information_container).to_be_visible(timeout=10000)
        logging.info("Checking visibility of product title")
        product_name = product_information_container.get_by_role("heading")
        expect(product_name).to_be_visible()
        for field in expected_fields:
            logging.info(f"Checking visibility of {field} field")
            expect(product_information_container.filter(has_text=field)).to_be_visible()

    def increase_quantity_by_arrow(self):
        """Click the arrow up button (simulate stepUp)"""
        self.page.evaluate(f'const input = document.querySelector("{self.QUANTITY_INPUT}"); input.stepUp();')

    def add_to_cart(self):
        self.safe_click(self.page.locator(self.ADD_TO_CART_BUTTON))

    def view_cart(self):
        self.safe_click(self.page.locator(self.VIEW_CART_LINK))
        return CartPage(self.page)
