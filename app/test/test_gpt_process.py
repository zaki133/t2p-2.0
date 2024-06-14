import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from gpt_process import ApiCaller
from config import API_KEY

class TestApiCaller(unittest.TestCase):
    @patch('gpt_process.openai.OpenAI')
    def setUp(self, mock_openai):
        # Mock the OpenAI client
        self.mock_client = MagicMock()
        mock_openai.return_value = self.mock_client

        # Initialize ApiCaller with a dummy API key
        self.api_caller = ApiCaller('dummy_api_key')

    def test_call_api(self):
        # Mock the chat.completions.create method
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices[0].message.content.strip.return_value = 'mock_response'
        self.mock_client.chat.completions.create.return_value = mock_chat_completion

        # Call the method and assert the response
        response = self.api_caller.call_api('system_prompt', 'user_text')
        self.assertEqual(response, 'mock_response')

    def test_call_api_error(self):
        # Mock the chat.completions.create method to raise an exception
        self.mock_client.chat.completions.create.side_effect = Exception('mock_exception')

        # Call the method and assert the response
        response = self.api_caller.call_api('system_prompt', 'user_text')
        self.assertEqual(response, 'An error occurred: mock_exception')




if __name__ == '__main__':
    unittest.main()