from api_clients.base_client import BaseAPIClient
from dotenv import load_dotenv
import os

load_dotenv()

AVAILABLE_OPENAI_MODELS = os.getenv('AVAILABLE_ANTHROPIC_MODELS').split(',')

class OpenAIClient(BaseAPIClient):
    """
    This class represents the OpenAI API client and inherits from the BaseAPIClient.
    It provides the implementation for sending requests to the OpenAI API.
    """

    def __init__(self, api_key, api_url):
        """
        Initialize the OpenAIClient with the API key and URL.

        Args:
            api_key (str): The OpenAI API key for authentication.
            api_url (str): The URL of the OpenAI API endpoint.
        """
        super().__init__(api_key, api_url)
        self.model = AVAILABLE_OPENAI_MODELS[0]  # Set the default model

    def _get_headers(self):
        """
        Return the headers required for the OpenAI API.
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def _get_request_data(self, prompt, chat_history):
        """
        Return the request data for the OpenAI API.
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
        Parse the response from the OpenAI API and return the AI's response and token usage.

        Returns:
            tuple: A tuple containing the AI's response (str) and a dictionary with input and output token counts.
        """
        response_data = response.json()

        # Extract the AI's response
        result = response_data.get('choices', [])[0].get('message', {}).get('content', '')

        # Extract token usage
        usage = response_data.get('usage', {})
        input_tokens = usage.get('prompt_tokens', 0)
        output_tokens = usage.get('completion_tokens', 0)

        return result or "No response received.", {"input_tokens": input_tokens, "output_tokens": output_tokens}



