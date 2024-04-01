# Terminal-Based Chat Application

This project is a terminal-based chat application that allows you to interact with various AI APIs, including Anthropic and OpenAI. The application provides a modular structure for easily switching between different AI chatbots and their respective models.

## Features

- Terminal-based user interface for chatting with AI models.
- Support for multiple AI chatbots (Anthropic and OpenAI).
- Ability to choose the AI chatbot and specific model to use.
- Modular architecture for easy extensibility and maintenance.
- Real-time pricing information and token usage tracking.
- Chat history saving (current saved in a temporary folder called `/chat_history`, generated locally when saving for the first time)
- Keyboard navigation for browsing chat history (WIP).
- Chat history saving and loading (WIP).

## Wish lists 

* [ ] OpenAI Client -- ChatGPT 
* [ ] Resume from a selected chat history.
* [ ] Navigate with keyboard keys (left-key, right-key, alt+left-key, right-left-key), while keeping the existing multi-line support. 

## Installation

1. Clone the repository

2. Navigate to the project directory

3. Install the required dependencies:
```
pip install -r requirements.txt 
```

## Setup

1. Create a `.env` file in the project root directory and add your API keys and configuration settings:
```
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
AVAILABLE_ANTHROPHIC_MODELS=claude-3-opus-20240229,claude-3-sonnet-20240229,claude-3-haiku-20240307
AVAILABLE_OPENAI_MODELS=gpt-3.5-turbo,gpt-4,gpt-4-turbo-preview
```
Replace `YOUR_ANTHROPIC_API_KEY` and `YOUR_OPENAI_API_KEY` with your actual API keys.
### Testing 

Run the tests:
```
python -m unittest tests/test_api_clients.py -v
```
The `-v` flag enables verbose output, which shows the status (pass or fail) of each test case.

The tests will load the API keys from the `.env` file and use them for testing the API client implementations. Make sure to set the API keys in the `.env` file before running the tests.

If you want to see more detailed output or stop the test runner after the first failure, you can use the `--failfast` option along with `--verbose`:
```
python -m unittest tests/test_api_clients.py -v --failfast
```
This will provide verbose output and stop the test runner as soon as the first test case fails, which can be helpful when debugging.

## Usage

1. Run the application

2. The application will prompt you to select an AI chatbot (Anthropic or OpenAI).

3. After selecting the AI chatbot, the application will prompt you to choose a specific model for that chatbot.

4. Once you've selected the model, you can start chatting with the AI by typing your messages in the terminal.

5. To submit a multi-line message, press enter to jump line and when you're ready to send the prompt, type `/send` on a new line after entering your message.

6. To exit the application, type `exit` on a new line (recommended) or `ctrl-c`

## Pricing Model

The application includes a real-time pricing feature that calculates the token costs for each conversation based on the selected AI model. The pricing information is displayed after each AI response, showing the cost for the current conversation and the total cost of all conversations.


## Project Structure 

```
chat_app/
├── api_clients/
│   ├── init.py
│   ├── anthropic_client.py
│   ├── base_client.py
│   └── openai_client.py
├── tests/
│   ├── init.py
│   └── test_api_clients.py
├── utils/
│   ├── init.py
│   └── file_utils.py
│   └── pricing_model.py
├── requirements.txt
├── app.py
└── README.md
```

- `api_clients/`: Contains the classes for different AI chatbots and API clients.
- `tests/`: Contains unit tests for the API client classes.
- `utils/`: Contains utility functions to calculate costs in $USD based on session usage token, save chat history to folder.
- `requirements.txt`: Lists the required Python dependencies.
- `chat_app.py`: The main Python file containing the entry point for the chat application.
- `README.md`: This file containing project information and instructions.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
