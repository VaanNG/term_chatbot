import os
from datetime import datetime

def save_chat_history(chat_history, folder_path="chat_history"):
    print('Entering saving chat history')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print('Folder made')
    
    now = datetime.now()
    filename = f"chat_history_{now.strftime('%Y%m%d_%H%M%S')}.md"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        for role, content in chat_history:
            if role == "user":
                file.write(f"**You:** {content}\n\n")
            elif role == "assistant":
                file.write(f"**AI:** {content}\n\n")

    print(f"Chat history saved to {file_path}")
