import logging
from endpoints.base_endpoint import BaseEndpoint

logger = logging.getLogger(__name__)

class ProductAPI(BaseEndpoint):

    @property
    def products(self):
        return self.response_json.get("products", [])

    def check_list_of_products_is_not_empty(self):
        logger.info("Checking the list of products is not empty")
        assert "products" in self.response_json
        assert isinstance(self.products, list)
        assert len(self.products) > 0
        return self

    def check_products_schema(self):
        logger.info("Checking the product schema")
        for product in self.products:
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "brand" in product
            assert "category" in product

            category = product["category"]
            assert "category" in category
            assert "usertype" in category
            assert "usertype" in category["usertype"]
        return self


