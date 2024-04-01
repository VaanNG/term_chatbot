import os
from dotenv import load_dotenv

# from api_clients.anthropic_chatbot import AnthropicChatbot
from api_clients.anthropic_client import AnthropicClient
from api_clients.openai_client import OpenAIClient 

# pricing & history
from utils.pricing_model import PricingModel
from utils.file_utils import save_chat_history
from utils.input_utils import get_user_input

# Load environment variables from .env file
load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

AVAILABLE_ANTHROPIC_MODELS = os.getenv('AVAILABLE_ANTHROPIC_MODELS').split(',')
AVAILABLE_OPENAI_MODELS = os.getenv('AVAILABLE_OPENAI_MODELS').split(',')

if not ANTHROPIC_API_KEY:
    print('error: ANTHROPIC_API_KEY environment variable is not set.')
    exit(1)

if not OPENAI_API_KEY:
    print('error: OPENAI_API_KEY environment variable is not set.')
    exit(1)

if not AVAILABLE_ANTHROPIC_MODELS:
    print('error: AVAILABLE_ANTHROPIC_MODELS environment variable is not set.')
    exit(1)

if not AVAILABLE_OPENAI_MODELS:
    print('error: AVAILABLE_OPENAI_MODELS environment variable is not set.')
    exit(1)


def main():
    print('Welcome to the AI Chat App!')
    print('Type "exit" to quit the application.')

    available_chatbots = {
        "1": ("Anthropic -- available", AnthropicClient, AVAILABLE_ANTHROPIC_MODELS),
        "2": ("OpenAI -- unavailable", OpenAIClient, AVAILABLE_OPENAI_MODELS)
    }

    print("Available AI chatbots:")
    for key, (chatbot_name, _, _) in available_chatbots.items():
        print(f"{key}. {chatbot_name}")

    chatbot_choice = input("Select an AI chatbot (enter the corresponding number): ")

    if chatbot_choice in available_chatbots:
        _, chatbot_class, available_models = available_chatbots[chatbot_choice]

        if chatbot_class == AnthropicClient:
            api_url = "https://api.anthropic.com/v1/messages"
            ai_chatbot = chatbot_class(api_key=ANTHROPIC_API_KEY, api_url=api_url)
        elif chatbot_class == OpenAIClient:
            api_url = "https://api.openai.com/v1/chat/completions"
            ai_chatbot = chatbot_class(api_key=OPENAI_API_KEY, api_url=api_url)

        print(f"Available models for {chatbot_class.__name__}:")
        for i, model in enumerate(available_models, start=1):
            print(f"{i}. {model}")

        model_index = input("Select a model (enter the corresponding number): ")
        try:
            model_index = int(model_index)
            if 1 <= model_index <= len(available_models):
                ai_chatbot.model = available_models[model_index - 1]
            else:
                raise ValueError
        except ValueError:
            print(f"Invalid model selection. Using the default model: {available_models[0]}")
            ai_chatbot.model = available_models[0]

        # begin chat
        total_input_tokens = 0
        total_output_tokens = 0
        pricing_model = PricingModel()
        total_cost = 0.0

        while True:
            try: 
                user_input = get_user_input()
                if user_input is None:
                    break

                if user_input.lower().strip() == 'exit':
                    break 

                response, token_usage = ai_chatbot.send_request(user_input)

                token_cost = pricing_model.get_token_cost(ai_chatbot.model, token_usage["input_tokens"], token_usage["output_tokens"])

                if token_cost is not None:
                    total_cost += token_cost 
                total_input_tokens += token_usage["input_tokens"]
                total_output_tokens += token_usage["output_tokens"]

                print('\nAI: ' + response + ' \n')
                print('!! TOKEN USAGE !!')
                if token_cost is not None:
                    print(f'Token usage: C:${token_cost:.2f}, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                else:
                    print(f'Token usage: C:$0.00, I:{token_usage["input_tokens"]}, O:{token_usage["output_tokens"]}')
                print(f'Total tokens: C:${total_cost:.2f}, I:{total_input_tokens}, O:{total_output_tokens}')
                print('!! TOKEN USAGE !!\n')

            except KeyboardInterrupt:
                print("Exiting...")
                break

        save_choice = input("Do you want to save the chat history? (y/n): ")
        if save_choice.lower() == 'y':
            save_chat_history(ai_chatbot.chat_history)
            print("Chat history saved. Goodbye! 👋✨")
        else:
            print("Chat history not saved. Goodbye! 👋✨")
        return None

    else:
        print("Invalid choice. Exiting...")

if __name__ == '__main__':
    main()

