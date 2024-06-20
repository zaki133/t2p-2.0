import unittest
import os
import sys
from unittest.mock import MagicMock

# Add the app/backend directory to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Use relative import for the app code.
from app import app
from backend.gpt_process import ApiCaller
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
        
    def test_api_call_error_500(self):
        """
        Test the api_call endpoint with a wrong content type. It should return a 500 error.
        """
        response = self.app.post('/api_call', "This is not json")
        self.assertEqual(response.status_code, 500)

    def test_api_call_success(self):
        """
        Test the api_call endpoint with a successful API call.
        """
        # Create a MagicMock instance
        mock_call_api = MagicMock(return_value='mock_response')
        mock_conversion_pipeline = MagicMock(return_value='mock_result')

        # Assign the MagicMock instances to the call_api and conversion_pipeline methods
        ApiCaller.call_api = mock_call_api
        ApiCaller.conversion_pipeline = mock_conversion_pipeline

        response = self.app.post('/api_call', json={"text": "Hello", "api_key": "dummy_api_key" })
        if response.status_code != 200:
            print(response.json)  # Print the response body when the test fails
        self.assertEqual(response.status_code, 200)
        mock_call_api.assert_called_once_with('system_prompt', 'user_text')

if __name__ == '__main__':
    unittest.main()