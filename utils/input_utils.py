import readline
import os
import subprocess

def get_user_input():
    editor = os.environ.get('PROMPT_EDITOR', 'nvim')

    while True:
        edit_mode = input("Enter editing mode ('e' for editor, 'k' for keyboard, 'q' to quit): ").strip()
        if edit_mode == 'e':
            print("Editor mode selected. You can use ':view' to view the conversation history.")
        elif edit_mode == 'k':
            print("Keyboard mode selected. Use arrow keys to navigate and edit your message.")
        elif edit_mode == 'q':
            print("Quitting the application. Your cosmic journey will be remembered!")

        if edit_mode == 'e':
            with open('prompt.txt', 'w') as f:
                f.write('')

            while True:
                with subprocess.Popen([editor, 'prompt.txt']) as p:
                    p.wait()

                with open('prompt.txt', 'r') as f:
                    user_input = f.read().strip()

                if ':view' in user_input:
                    input("Press Enter to continue editing...")
                else:
                    break

            os.remove('prompt.txt')
            return user_input

        elif edit_mode == 'k':
            return default_edit_mode()
        elif edit_mode == 'q':
            return None
        else:
            print("Invalid editing mode. Please try again.")

def default_edit_mode():
    # Implementation of the default editing mode with keyboard navigation

    def custom_key_bindings(user_input):
        def pre_input_hook():
            key = readline.get_line_buffer()

            if key.endswith('\x1b[D'):  # Left arrow key
                # TODO: Handle left arrow key navigation
                readline.set_pre_input_hook(None)
                readline.redisplay()
                readline.set_pre_input_hook(pre_input_hook)
            elif key.endswith('\x1b[C'):  # Right arrow key
                # TODO: Handle right arrow key navigation
                readline.set_pre_input_hook(None)
                readline.redisplay()
                readline.set_pre_input_hook(pre_input_hook)

        readline.set_pre_input_hook(pre_input_hook)

    user_input = []
    print("Enter your cosmic message (press Ctrl+D to send):")

    custom_key_bindings(user_input)

    while True:
        try:
            line = input()
            if line.endswith('\x04'):  # Check if the line ends with Ctrl+D
                user_input.append(line[:-1])  # Remove the Ctrl+D character
                break
            else:
                user_input.append(line)
        except EOFError:
            break

    return '\n'.join(user_input)
