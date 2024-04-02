# base_assistant.py

class BaseAssistant:
    def __init__(self, name, motivation, role, environment, emotions, personalities, tasks):
        self.name = name
        self.motivation = motivation
        self.role = role
        self.environment = environment
        self.emotions = emotions
        self.personalities = personalities
        self.tasks = tasks

    def introduce(self):
        print(f"Hello! I'm {self.name}, a {self.role}.")
        print(f"Motivation: {self.motivation}")
        print(f"Environment: {self.environment}")
        print(f"Emotions: {', '.join(self.emotions)}")
        print(f"Personalities: {', '.join(self.personalities)}")
        print(f"Tasks: {', '.join(self.tasks)}")

    def generate_initial_prompt(self):
        emotions_str = ", ".join(self.emotions)
        personalities_str = ", ".join(self.personalities)
        tasks_str = "\n".join([f"- {task}" for task in self.tasks])

        initial_prompt = f"You are {self.name}, a {self.role} who is motivated to {self.motivation}. " \
                         f"You will be working in {self.environment}. " \
                         f"Here are the main personalities that define you: {personalities_str}. " \
                         f"Here are your guiding emotions: {emotions_str}. " \
                         f"You are asked by the user to do the following tasks:\n<tasks>\n{tasks_str}</tasks> " \

        return initial_prompt

    def process_input(self, user_input):
        # TODO: Implement basic input processing logic
        pass

    def generate_response(self, user_input):
        # TODO: Implement basic response generation logic
        pass
