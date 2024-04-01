# user input
def get_user_input():
    """
    Get multi-line user input until the '/send' command is encountered.
    """
    user_input = []
    print("Enter your message (type '/send' on a new line to send):")
    first_line = True
    while True:
        try:
            if first_line:
                line = input("You: ")
                first_line = False
            else:
                line = input()
        except KeyboardInterrupt:
            print("\nExiting...")
            return None
        if line.strip() == "/send":
            break
        user_input.append(line)
    return "\n".join(user_input)
