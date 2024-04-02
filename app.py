import os
import json
import logging
from dotenv import load_dotenv
from api_clients.anthropic_client import AnthropicClient
from api_clients.openai_client import OpenAIClient
from utils.pricing_model import PricingModel
from utils.file_utils import save_chat_history
from utils.input_utils import get_user_input
from utils.time_utils import get_current_time
from assistants.coding_assistant import CodingAssistant

# Logging configuration 
logging.basicConfig(
        filename='app.log'
        , level=logging.INFO
        , format='%(asctime)s - %(levelname)s - %(message)s'
        , datefmt='%Y-%m-%d %H:%M:%S'
        )

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

AVAILABLE_ANTHROPIC_MODELS = os.getenv('AVAILABLE_ANTHROPIC_MODELS').split(',')
AVAILABLE_OPENAI_MODELS = os.getenv('AVAILABLE_OPENAI_MODELS').split(',')

def load_assistant_config(assistant_type):
    config_file = f"config/{assistant_type}_config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def main():
    logging.info('Starting the chat application...')
    print('Welcome to the AI Chat App!')
    print('Type "exit" to quit the application.')

    available_chatbots = {
        "1": ("Anthropic 🟢", AnthropicClient),
        "2": ("OpenAI 🟢", OpenAIClient)
    }

    print("Available AI chatbots:")
    for key, (chatbot_name, _) in available_chatbots.items():
        print(f"{key}. {chatbot_name}")

    try:
        chatbot_choice = input("Select an AI chatbot (enter the corresponding number): ")
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted. Exiting the chat application.')
        print('\nKeyboard Interrupted. Exiting the chat application.')
        return None

    if chatbot_choice in available_chatbots:
        _, chatbot_class = available_chatbots[chatbot_choice]

        try:
            if chatbot_class == AnthropicClient:
                api_url = "https://api.anthropic.com/v1/messages"
            elif chatbot_class == OpenAIClient:
                api_url = "https://api.openai.com/v1/chat/completions"

            if chatbot_class == AnthropicClient:
                ai_chatbot = chatbot_class(api_key=ANTHROPIC_API_KEY, api_url=api_url)
            elif chatbot_class == OpenAIClient:
                ai_chatbot = chatbot_class(api_key=OPENAI_API_KEY, api_url=api_url)

            print(f"Available models for {chatbot_class.__name__}:")
            available_models = AVAILABLE_ANTHROPIC_MODELS if chatbot_class == AnthropicClient else AVAILABLE_OPENAI_MODELS
            for i, model in enumerate(available_models, start=1):
                print(f"{i}. {model}")

            model_index = input("Select a model (enter the corresponding number): ")

        except KeyboardInterrupt:
            logging.info('Keyboard Interrupted. Exiting the chat application.')
            print('\nKeyboard Interrupted. Exiting the chat application.')
            return None

        try:
            model_index = int(model_index)
            if 1 <= model_index <= len(available_models):
                ai_chatbot.model = available_models[model_index - 1]
            else:
                raise ValueError
        except ValueError:
            print(f"Invalid model selection. Using the default model: {available_models[0]}")
            ai_chatbot.model = available_models[0]

        # init variables
        total_input_tokens = 0
        total_output_tokens = 0
        pricing_model = PricingModel()
        total_cost = 0.0

        use_assistant = input("Do you want to use an AI assistant? (y/n): ")

        if use_assistant.lower().strip() == 'y':
            available_assistants = {
                "1": "CodingAssistant",
            }

            print("Available AI assistants:")
            for key, assistant_type in available_assistants.items():
                print(f"{key}. {assistant_type}")

            assistant_choice = input("Select an AI assistant (enter the corresponding number): ")

            if assistant_choice in available_assistants:
                assistant_type = available_assistants[assistant_choice]
                config = load_assistant_config(assistant_type)

                name = config["name"]
                motivation = config["motivation"]
                role = config["role"]
                environment = config["environment"]
                emotions = config["emotions"]
                personalities = config["personalities"]

                tasks_input = input("Enter the tasks for the assistant (comma-separated): ")
                tasks = [task.strip() for task in tasks_input.split(",")]

                if assistant_type == "CodingAssistant":
                    print("Enter the path to the coding project folder: ")
                    project_folder = get_user_input()
                    assistant = CodingAssistant(name=name, motivation=motivation, role=role,
                                                environment=environment, emotions=emotions,
                                                personalities=personalities, tasks=tasks, 
                                                project_folder=project_folder)
                    assistant.introduce()
                    assistant.process_project_folder()
                else:
                    # TODO: Implement other specialized assistants
                    pass

                # sending intial prompt
                initial_prompt = assistant.generate_initial_prompt()
                print(f'\n{get_current_time()} Intial Prompt: \n{initial_prompt}\n')
                try:
                    response, token_usage = ai_chatbot.send_request(initial_prompt)
                except Exception as e:
                    logging.error(f'Error occurred: {str(e)}')
                    print('An unexpected error occured. Please check the log file for more details.')
                    return None

                token_cost = pricing_model.get_token_cost(ai_chatbot.model, token_usage["input_tokens"], token_usage["output_tokens"])

                if token_cost is not None:
                    total_cost += token_cost
                total_input_tokens += token_usage["input_tokens"]
                total_output_tokens += token_usage["output_tokens"]

                print(f'\n{get_current_time()} AI 💡: ' + response + ' \n')
                print('!! TOKEN USAGE !!')
                if token_cost is not None:
                    print(f'Token usage: C:💵{token_cost:.5f}$, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                else:
                    print(f'Token usage: C:💵0.00000$, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                print(f'Total tokens: C:💵{total_cost:.5f}$, I:{total_input_tokens}, O:{total_output_tokens}')
                print('!! TOKEN USAGE !!\n')

            else:
                print("Invalid assistant choice. Exiting...")
        else:
            print("No assistant selected. Proceeding with the chatbot only.\n")
        # start chat loop
        try:
            while True:
                try:
                    user_input = get_user_input()
                    if user_input is None:
                        break

                    if user_input.lower().strip() == 'exit':
                        break

                    print(f'\n{get_current_time()} User 🕯️ : ' + user_input)
                    response, token_usage = ai_chatbot.send_request(user_input)

                    token_cost = pricing_model.get_token_cost(ai_chatbot.model, token_usage["input_tokens"], token_usage["output_tokens"])

                    if token_cost is not None:
                        total_cost += token_cost
                    total_input_tokens += token_usage["input_tokens"]
                    total_output_tokens += token_usage["output_tokens"]

                    print(f'\n{get_current_time()} AI 💡: ' + response + ' \n')
                    print('!! TOKEN USAGE !!')
                    if token_cost is not None:
                        print(f'Token usage: C:💵{token_cost:.5f}$, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                    else:
                        print(f'Token usage: C:💵0.00000$, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                    print(f'Total tokens: C:💵{total_cost:.5f}$, I:{total_input_tokens}, O:{total_output_tokens}')
                    print('!! TOKEN USAGE !!\n')

                except KeyboardInterrupt:
                    print("Exiting...")
                    logging.info('Exiting due to keyboard interrupt.')
                    break

        except Exception as e:
            logging.error(f'Error occurred: {str(e)}')
            print('An unexpected error occured. Please check the log file for more details.')

        save_choice = input("Do you want to save the chat history? (y/n): ")
        if save_choice.lower() == 'y':
            save_chat_history(ai_chatbot.chat_history)
            print("Chat history saved. Goodbye! 👋✨")
        else:
            print("Chat history not saved. Goodbye! 👋✨")
        logging.info('Exiting the chat application')
        return None

    else:
        print("Invalid chatbot choice. Exiting...")
        logging.info('Invalid chatbot choice. Exiting the chat application.')


if __name__ == '__main__':
    main()
