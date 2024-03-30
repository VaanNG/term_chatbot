from api_clients.base_client import BaseAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

AVAILABLE_ANTHROPIC_MODELS = os.getenv('AVAILABLE_ANTHROPIC_MODELS').split(',')

class AnthropicHTTPClient(BaseAPIClient):
    """
    This class represents the Anthropic API client using direct HTTP requests.
    It inherits from the BaseAPIClient and provides the implementation for sending requests to the Anthropic API.
    """

    def __init__(self, api_key, api_url="https://api.anthropic.com/v1/messages"):
        """
        Initialize the AnthropicHTTPClient with the API key and URL.

        Args:
            api_key (str): The Anthropic API key for authentication.
            api_url (str): The URL of the Anthropic API endpoint (default: "https://api.anthropic.com/v1/messages").
        """
        super().__init__(api_key, api_url)
        self.model = AVAILABLE_ANTHROPIC_MODELS[0]  # Set the default model

    def _get_headers(self):
        """
        Return the headers required for the Anthropic API.
        """
        return {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key,
            'Anthropic-Version': '2023-06-01'
        }

    def _get_request_data(self, prompt, chat_history):
        """
        Return the request data for the Anthropic API.
        """
        messages = []
        for role, content in chat_history:
            messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": prompt})

        return {
            'model': self.model,
            'max_tokens': 1000,  # Adjust as needed
            'messages': messages
        }

    def _parse_response(self, response):
        """
         Parse the response from the Anthropic API and return the AI's response and token usage.

        Returns:
            tuple: A tuple containing the AI's response (str) and a dictionary with input and output token counts.
        """
        response_data = response.json()
        content_blocks = response_data.get('content', [])
        result = ''
        for block in content_blocks:
            if block.get('type') == 'text':
                result += block.get('text', '')
            elif block.get('type') == 'code':
                result += f"```\n{block.get('code', '')}\n```"
            # Add other block types as needed

        usage = response_data.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)

        return result or "No response received.", {"input_tokens": input_tokens, "output_tokens": output_tokens}
