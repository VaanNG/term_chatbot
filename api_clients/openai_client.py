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

    def _get_request_data(self, prompt):
        """
        Return the request data for the OpenAI API.
        """
        return {
            'prompt': prompt,
            'model': self.model,
            'max_tokens': 1000  # Adjust as needed
        }

    def _parse_response(self, response):
        """
        Parse the response from the OpenAI API and return the AI's response.
        """
        return response.json()['choices'][0]['text']
