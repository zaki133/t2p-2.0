import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app import ApiCaller
from config import API_KEY

class TestApiCaller(unittest.TestCase):
    def setUp(self):
        self.api_key = API_KEY
        self.api_caller = ApiCaller(self.api_key)

    def test_run_success(self):
        """
        Test case to verify the successful execution of the `run` method in the API caller.

        It mocks the completion response from the OpenAI API and asserts that the response
        matches the expected generated text. It also verifies that the `create` method of
        the OpenAI API client is called with the correct parameters.
        """
        expected_response = "Generated text"
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content.strip.return_value = expected_response
        mock_create = MagicMock(return_value=mock_completion)

        with patch.object(self.api_caller.client.chat.completions, 'create', mock_create):
            response = self.api_caller.run("User input")

        self.assertEqual(response, expected_response)
        mock_create.assert_called_once_with(
            messages=[{"role": "user", "content": "User input"}],
            model="gpt-4-turbo",
            max_tokens=4096
        )

    def test_run_error(self):
        """
        Test case to verify the behavior when an error occurs during API call.

        The test simulates an API call failure by raising an exception with the message "API call failed".
        It uses a MagicMock object to mock the API call and raise the exception.
        The expected behavior is that the `run` method of `api_caller` should return the expected error message.

        """
        expected_error = "An error occurred: API call failed"
        mock_create = MagicMock(side_effect=Exception("API call failed"))

        with patch.object(self.api_caller.client.chat.completions, 'create', mock_create):
            response = self.api_caller.run("User input")

        self.assertEqual(response, expected_error)
        mock_create.assert_called_once_with(
            messages=[{"role": "user", "content": "User input"}],
            model="gpt-4-turbo",
            max_tokens=4096
        )

if __name__ == '__main__':
    unittest.main()