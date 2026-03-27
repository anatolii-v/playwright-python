import logging
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class TestCasesPage(BasePage):

    def check_that_test_cases_are_present(self):
        logger.info("Checking the the list of test cases is not empty")
        number_of_test_cases_on_the_page = self.page.get_by_role("link").filter(has_text="Test Case ").count()
        logger.info(f"Number of test cases is {number_of_test_cases_on_the_page}")
        assert number_of_test_cases_on_the_page > 0, "The are no test cases available!"
