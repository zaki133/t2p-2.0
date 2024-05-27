import unittest
import os
import sys

# Add the app/backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Use relative import for the app code
from app import app
from config import API_KEY
# The following is the test for the app.py file
class TestApp(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    # Test to check if the app responds with a 200 status code
    def test_test_connection(self):
        response = self.app.get('/test_connection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Successful")

    # Missing data test
    def test_api_call_missing_data(self):
        response = self.app.post('/api_call', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing data for: text, api_key"})

    # Test to check if the app responds with a 200 status code when the API Key is correct    
    def test_api_call_success(self):
        # Please be careful don't commit your API key to a public repository
        response = self.app.post('/api_call', json={"text": "Hello", "api_key": API_KEY})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": "Processed data"})

    # Test to check if the app responds with a 500 status code when an exception is raised    
    def test_api_call_exception(self):
        response = self.app.post('/api_call', json={"text": "Hello", "api_key": "12345"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Exception message"})
        

if __name__ == '__main__':
    unittest.main()