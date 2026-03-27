import logging
from pages.base_page import BasePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

class ProductsPage(BasePage):

    SEARCH_PRODUCT_FIELD = {"role": "textbox", "name": "Search Product"}
    SEARCHED_PRODUCT_TITLE = ".product-overlay p"
    SUBMIT_BUTTON = "#submit_search"
    PRODUCT_CARD = ".features_items .col-sm-4"
    ADD_TO_CART_BUTTON = ".overlay-content a.add-to-cart"
    CONTINUE_SHOPPING = "Continue Shopping"
    VIEW_CART_LINK = {"role": "link", "name": "View Cart"}
    

    def go_to_first_product_details(self):
        logging.info("Navigating to first product details page")
        details_link = self.page.locator("a[href*='/product_details/']").first
        expect(details_link).to_be_visible(timeout=10000)
        self.safe_click(details_link)
        self.page.wait_for_url("**/product_details/**", timeout=60000)
        return ProductPage(self.page)
    
    def search_product(self, product_name):
        logging.info(f"Searchig for product {product_name}")
        self.page.get_by_role(**self.SEARCH_PRODUCT_FIELD).fill(product_name)
        self.safe_click(self.page.locator(self.SUBMIT_BUTTON))

    def check_that_searched_product_is_visible(self, product_name):
        logging.info(f"Checking the product {product_name} is visible")
        expect(self.page.locator(self.SEARCHED_PRODUCT_TITLE)).to_contain_text(product_name)

    def add_product(self, number):
        product_cart = self.page.locator(self.PRODUCT_CARD).nth(number)
        self.safe_hover(product_cart)
        add_to_cart_button = product_cart.locator(self.ADD_TO_CART_BUTTON)
        expect(add_to_cart_button).to_be_visible()
        self.safe_click(add_to_cart_button)

    def add_first_product(self):
        logging.info("Adding the first product on the page")
        self.add_product(0)

    def add_second_product(self):
        logging.info("Adding the second product on the page")
        self.add_product(1)

    def continue_shoping(self):
        logging.info("Continue shopping")
        continue_shopping_button = self.page.get_by_text(self.CONTINUE_SHOPPING)
        expect(continue_shopping_button).to_be_visible()
        self.safe_click(continue_shopping_button)

    def open_cart(self):
        self.safe_click(self.page.get_by_role(**self.VIEW_CART_LINK))
        return CartPage(self.page)
