import readline
import os
import time

def get_user_input():
    editor = os.environ.get('PROMPT_EDITOR', 'nvim')
    marker = 'send'

    while True:
        edit_mode = input("Enter editing mode ('e' for editor, 'k' for keyboard, 'q' to quit): ")

        if edit_mode == 'e':
            print("Type 'send; on a new line to send message.")
            with open('prompt.txt', 'w') as f:
                f.write('')

            # Open tmux and split the screen
            os.system('tmux split-window -v && tmux resize-pane -D 10')
            os.system(f'tmux send-keys "{editor} prompt.txt; echo {marker} >> prompt.txt" C-m')

            # Wait for the marker to appear in the file
            while True:
                with open('prompt.txt', 'r') as f:
                    content = f.read().strip()
                    if content.endswith(f"\n{marker}"):
                        break
                time.sleep(0.1)

            # Kill the tmux window
            os.system('tmux kill-pane')

            if os.path.exists('prompt.txt'):
                with open('prompt.txt', 'r') as f:
                    user_input = f.read().strip().replace(f'\n{marker}', '').strip()
                os.remove('prompt.txt')
            else:
                user_input = ''

            if user_input:
                print('User: ' + user_input)
                return user_input
            else:
                print("No input provided. Exiting gracefully.")
                return None

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
    print("Enter your cosmic message (press Ctrl+d on a new line to send):")

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
