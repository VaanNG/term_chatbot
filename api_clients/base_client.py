import requests

class BaseAPIClient:
    """
    This is a base class that provides common functionality for different AI API clients
    that make direct HTTP requests.
    """

    def __init__(self, api_key, api_url):
        """
        Initialize the BaseAPIClient with the API key and URL.

        Args:
            api_key (str): The API key for authentication.
            api_url (str): The URL of the API endpoint.
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = self._get_headers()
        self.chat_history = []  # Initialize an empty chat history

    def send_request(self, prompt):
        """
        Send a request to the API with the given prompt and return the response.

        Args:
            prompt (str): The prompt to send to the AI.

        Returns:
            tuple: A tuple containing the AI's response (str) and a dictionary with input and output token counts.
        """
        data = self._get_request_data(prompt, self.chat_history)
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        ai_response, token_usage = self._parse_response(response)
        self.update_chat_history(prompt, ai_response)
        return ai_response, token_usage

    def update_chat_history(self, prompt, ai_response):
        """
        Update the chat history with the user's prompt and the AI's response.

        Args:
            prompt (str): The user's prompt.
            ai_response (str): The response from the AI.
        """
        self.chat_history.append(("user", prompt))
        self.chat_history.append(("assistant", ai_response))

    def _get_request_data(self, prompt):
        """
        This method should be implemented by the subclasses to return the appropriate request data
        for the specific API.

        Args:
            prompt (str): The prompt to send to the AI.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError("_get_request_data method must be implemented")

    def _parse_response(self, response):
        """
        This method should be implemented by the subclasses to parse the response from the API
        and return the AI's response.

        Args:
            response (requests.Response): The response object from the API.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError("_parse_response method must be implemented")
