import unittest
import os
import sys
import logging

# Add the app/backend directory to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Use relative import for the app code.
from app import app
from config import API_KEY
# The following is the test for the app.py file.
class TestApp(unittest.TestCase):
    """
    This class contains unit tests for the app.
    """

    def setUp(self):
        """
        Set up the test client.
        """
        self.app = app.test_client()
        self.app.testing = True
        
    def test_test_connection(self):
        """
        Test the test_connection endpoint. It should return "Successful".
        """
        response = self.app.get('/test_connection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Successful")

    def test_api_call_missing_data(self):
        """
        Test the api_call endpoint with missing data. It should return a 400 error.
        """
        response = self.app.post('/api_call', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing data for: text, api_key"})

    def test_api_call_success(self):
        """
        Test the api_call endpoint with a successful API call. It should return the generated text.
        Please insert your API key in the config.py file.
        """
        response = self.app.post('/api_call', json={"text": "Hello", "api_key": API_KEY})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hello" in response.json["result"])
        
    def test_api_call_error_500(self):
        """
        Test the api_call endpoint with a wrong content type. It should return a 500 error.
        """
        response = self.app.post('/api_call', "This is not json")
        log = logging.getLogger("TestApp.test_api_call_error_500")
        log.debug("Status code: " + str(response.status_code))
        log.debug("Error text: " + str(response.json))
        self.assertEqual(response.status_code, 500)

    def test_api_call_error_message(self):
        """
        Test the api_call endpoint with wrong api key. It should return a 500 error.
        """
        response = self.app.post('/api_call', json={"text": "Error", "api_key": "wrong_key"})
        self.assertEqual(response.status_code, 500)
        self.assertTrue("'error': {'message':" in response.json["error"])

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestApp.test_api_call_error_500").setLevel(logging.DEBUG)
    unittest.main()