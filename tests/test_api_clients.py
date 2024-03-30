import unittest
from unittest.mock import patch, Mock
from api_clients.anthropic_client import AnthropicHTTPClient, AVAILABLE_ANTHROPIC_MODELS
from api_clients.openai_client import OpenAIClient, AVAILABLE_OPENAI_MODELS



class TestAPIClients(unittest.TestCase):
    """
    This class contains unit tests for the API client classes.
    """

    def test_anthropic_http_client_headers(self):
        """
        Test the headers returned by the AnthropicHTTPClient.
        """
        api_key = 'test-api-key'
        client = AnthropicHTTPClient(api_key=api_key, api_url='https://api.anthropic.com/v1/messages')

        expected_headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key,
            'Anthropic-Version': '2023-06-01'
        }

        self.assertEqual(client._get_headers(), expected_headers)

    def test_anthropic_http_client_request_data(self):
        """
        Test the request data constructed by the AnthropicHTTPClient.
        """
        client = AnthropicHTTPClient(api_key='test-api-key', api_url='https://api.anthropic.com/v1/messages')
        client.model = AVAILABLE_ANTHROPIC_MODELS[0]  # Select the first available model
        prompt = 'Hello, world!'
        chat_history = []

        expected_request_data = {
            'model': AVAILABLE_ANTHROPIC_MODELS[0],
            'max_tokens': 1000,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }

        self.assertEqual(client._get_request_data(prompt, chat_history), expected_request_data)

    @patch('requests.post')
    def test_anthropic_client(self, mock_post):
        """
        Test the AnthropicHTTPClient by mocking the requests.post method.
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": [
                {
                    "type": "text",
                    "text": "This is a test response from the AI."
                }
            ],
            "usage": {  # Include this if your method processes token usage 
                "input_tokens": 5,
                "output_tokens": 30
            } 
        }

        mock_post.return_value = mock_response

        api_key ='test-api-key' 
        api_url = 'https://api.anthropic.com/v1/messages'
        client = AnthropicHTTPClient(api_key=api_key, api_url=api_url)
        client.model = AVAILABLE_ANTHROPIC_MODELS[0]  # Select the first available model

        response = client.send_request('Hello')

        self.assertEqual(response[0], 'This is a test response from the AI.')

    # @patch('requests.post')
    # def test_openai_client(self, mock_post):
    #     """
    #     Test the OpenAIClient by mocking the requests.post method.
    #     """
    #     mock_response = Mock()
    #     mock_response.json.return_value = {'choices': [{'text': 'Hello, world!'}]}
    #     mock_post.return_value = mock_response
    #
    #     api_key = 'test_key'
    #     api_url = 'https://api.openai.com/v1/engines/davinci/completions'
    #     client = OpenAIClient(api_key=api_key, api_url=api_url)
    #     client.model = AVAILABLE_OPENAI_MODELS[0]  # Select the first available model
    #
    #     response = client.send_request('Hello')
    #
    #     self.assertEqual(response, 'Hello, world!')

if __name__ == '__main__':
    unittest.main()
