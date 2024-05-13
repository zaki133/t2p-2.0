import unittest
# Use relative import for the app code
from app import app
class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_test_connection(self):
        response = self.app.get('/test_connection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "Successful")

if __name__ == '__main__':
    unittest.main()

