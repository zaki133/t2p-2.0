import unittest
# Use relative import for the app code
from app import app
# The following is the test case for the app.py file
class TestApp(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    # This test checks if the connection to the /test_connection endpoint is successful
    def test_test_connection(self):
        response = self.app.get('/test_connection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Successful")

if __name__ == '__main__':
    unittest.main()