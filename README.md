# Terminal-Based Chat Application

This project is a terminal-based chat application that allows you to interact with various AI APIs, including Anthropic and OpenAI. The application provides a modular structure for easily switching between different AI chatbots and their respective models.

## Features

- Terminal-based user interface for chatting with AI models.
- Support for multiple AI chatbots (Anthropic and OpenAI).
- Ability to choose the AI chatbot and specific model to use.
- Modular architecture for easy extensibility and maintenance.
- Real-time pricing information and token usage tracking.
- Chat history saving (current saved in a temporary folder called `/chat_histories`, generated locally when saving for the first time)
- Send messages by selecting between different editing modes: terminal editor or keyboard.
- Support for specialized AI assistants, such as the `CodingAssistant`, which can provide guidance and suggestions for coding projects.

## Installation

1. Clone the repository

2. Navigate to the project directory

3. Assuming you already have python installed, run the script `env.sh`:
```bash
source env.sh
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
### Testing (in development) 

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

1. Run the application by running the below commands
```bash
source env.sh # Starting the virtual env
python app.py # Starting the app
```
2. The application will prompt you to select an AI chatbot (Anthropic or OpenAI).

3. After selecting the AI chatbot, the application will prompt you to choose a specific model for that chatbot.

4. Once you've selected the model, you can start chatting with the AI by typing your messages in the terminal.

5. To submit a multi-line message, press enter to jump line and when you're ready to send the prompt, type `/send` on a new line after entering your message.

6. To exit the application, type `exit` on a new line (recommended) or `ctrl-c`

## Editing Modes 🎨⌨️

The AI Chat App now supports two editing modes: Editor Mode and Keyboard Mode.

### Editor Mode ✍️🌟
*in order to use this mode, it is recommended that you have tmux installed.*
- Trigger the Editor Mode by entering 'e' when prompted for the editing mode.
- The app will open a `tmux` pane with your preferred editor (default: `nvim`).
- Edit your message in the editor, and type 'send' on a new line to send the message.
- If you close the editor without providing any input, the app will gracefully exit the editing mode.

### Keyboard Mode ⌨️💬
- Trigger the Keyboard Mode by entering 'k' when prompted for the editing mode.
- Type your message directly in the terminal, using the keyboard for navigation and editing.
- Press `Ctrl+D` on a new line to send the message.

## Chat History Saving 💾✨
- When exiting the app, you will be prompted to choose whether to save the chat history.
- Enter 'y' to save the chat history or 'n' to exit without saving.
- The chat history will be saved in a designated directory for future reference.

## Pricing Model

The application includes a real-time pricing feature that calculates the token costs for each conversation based on the selected AI model. The pricing information is displayed after each AI response, showing the cost for the current conversation and the total cost of all conversations.

## Assistants 

## Customer config 

You can edit the .json config in the `./config/` folder to tweak the Assistants.

### Coding Assistant

The chat application now includes a specialized `CodingAssistant` that can provide guidance and suggestions for coding projects. The `CodingAssistant` is a subclass of the `BaseAssistant` and has the following capabilities:

- Processes the content of a provided coding project folder, ignoring files specified in a `.gitignore` file.
- Generates an initial prompt that introduces the assistant, its role, environment, emotions, and the tasks it has been assigned.
- Utilizes the project files and the assistant's coding knowledge to assist the user with their coding tasks.
- Provides recommendations and code snippets to the user, without direct interaction with the project files.

To use the `CodingAssistant`, the user needs to provide the path to the coding project folder when prompted during the application startup.

## Project Structure 

``` 
chat_app/
├── api_clients/
│   ├── __init__.py
│   ├── anthropic_client.py
│   ├── base_client.py
│   └── openai_client.py
├── assistants/
│   ├── __init__.py
│   ├── base_assistant.py
│   └── coding_assistant.py
├── config/
│   ├── CodingAssistant_config.json
├── tests/
│   ├── __init__.py
│   └── test_api_clients.py
├── utils/
│   ├── __init__.py
│   ├── input_utils.py
│   └── file_utils.py
│   └── pricing_model.py
├── requirements.txt
├── app.py
└── README.md
```

- `api_clients/`: Contains the classes for different AI chatbots and API clients.
- `assistants/`: Contains the base assistant class (`BaseAssistant`) and specialized assistant implementations, such as the `CodingAssistant`.
- `tests/`: Contains unit tests for the API client classes.
- `utils/`: Contains utility functions to calculate costs in $USD based on session usage token, save chat history to folder.
- `requirements.txt`: Lists the required Python dependencies.
- `chat_app.py`: The main Python file containing the entry point for the chat application.
- `README.md`: This file containing project information and instructions.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
