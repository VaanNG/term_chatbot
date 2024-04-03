import json
import os
from datetime import datetime 

def save_chat_history(self, directory="chat_histories"):
    """Saves the chat history to a JSON file in the specified directory.

    Args:
        directory (str, optional): The directory to save the chat history. Defaults to "chat_histories".
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.json"
    filepath = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Ensure that any context is also saved
    if "context" not in self.chat_history:  
        self.chat_history["context"] = {}

    with open(filepath, "w") as f:
        json.dump(self.chat_history, f, indent=4)  
