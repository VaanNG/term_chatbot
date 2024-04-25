import json
import os
from datetime import datetime 

def save_chat_history(self, directory="chat_histories"):
    """Saves the chat history to a JSON file and as a Markdown file in the specified directory.

    Args:
        directory (str, optional): The directory to save the chat history. Defaults to "chat_histories".
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}"
    filepath = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Ensure that any context is also saved
    if "context" not in self.chat_history:  
        self.chat_history["context"] = {}

    with open(filepath + '.json', "w") as f:
        json.dump(self.chat_history, f, indent=4)  

    with open(filepath + '.md', "w") as f:
        for message in self.chat_history['messages']:
            if message['sender'] == 'user':
                f.write(f"**User ({message['timestamp']}):** {message['text']}\n\n")
            else:  
                f.write(f"**Assistant ({message['timestamp']}):** {message['text']}\n\n") 
