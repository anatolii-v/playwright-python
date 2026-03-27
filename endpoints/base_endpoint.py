import logging

logger = logging.getLogger(__name__)

class BaseEndpoint:

    BASE_URL = "https://automationexercise.com/api"

    def __init__(self):
        self.response = None
        self.response_json = None

    def check_http_status(self, expected_code):
        logger.info(f"Checking that the http status code of the response is {expected_code}")
        assert self.response is not None, "Response is not set"
        actual_status_code = self.response.status_code
        assert actual_status_code == expected_code, f"The actual http status: {actual_status_code}"
        return self

    def check_message_from_response_json(self, expected_message):
        logger.info(f"Checking that the message in the response is: {expected_message}")
        assert self.response_json is not None, "Response is not set"
        actual_message = self.response_json["message"]
        assert actual_message == expected_message, f"The actual message: {actual_message}"
        return self

    def check_status_code_from_response_json(self, expected_code):
        logger.info(f"Checking that the status code in the response is {expected_code}")
        assert self.response_json is not None, "Response is not set"
        actual_code = self.response_json["responseCode"]
        assert actual_code == expected_code, f"The actual code: {actual_code}"
        return self
