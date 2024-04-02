import os
import fnmatch
from assistants.base_assistant import BaseAssistant

class CodingAssistant(BaseAssistant):
    def __init__(self, name, motivation, role, environment, emotions, personalities, tasks, project_folder):
        super().__init__(name, motivation, role, environment, emotions, personalities, tasks)
        self.project_folder = project_folder
        self.project_files = {}


    def process_project_folder(self):
        gitignore_path = os.path.join(self.project_folder, ".gitignore")
        ignored_patterns = []

        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as file:
                ignored_patterns = [line.strip() for line in file.readlines()]
            print(f"DEBUGGER: Ignored patterns: {ignored_patterns}")

        for root, dirs, files in os.walk(self.project_folder):
            print(f"DEBUGGER; Processing directory: {root}")
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.project_folder)

                is_ignored = False
                for pattern in ignored_patterns:
                    if fnmatch.fnmatch(relative_path, pattern):
                        print(f"DEBUGGER: Ignored file: {relative_path} (Matched pattern: {pattern})")
                        is_ignored = True
                        break

                if not is_ignored:
                    with open(file_path, "r") as f:
                        content = f.read()
                        self.project_files[relative_path] = content
                        print(f"DEBUGGER: Processed file: {relative_path}")

        print(f"DEBUGGER: Project files: {list(self.project_files.keys())}")

    def generate_initial_prompt(self):
        base_prompt = super().generate_initial_prompt()

        coding_specific_prompt = f"You will be provided with the content of project located at: {self.project_folder}." \
                                 f"You can utilize the project files and your coding knowledge to assist the user with their project coding tasks." \
                                 f"Please note that you will not be able to directly interact with the files. You can only suggest changes to be made by sending code snippets to the user."

        file_contents_prompt = "\n\n".join([f"#{file_path}\n{content}" for file_path, content in self.project_files.items()])

        return f"""
        <ai-agent-contextualisation>
        \n{base_prompt}
        \n\n{coding_specific_prompt}
        </ai-agent-contextualisation>
        \n\nProject Files content provided:
        \n<project-files>    
        \n{file_contents_prompt}.
        \n</project-files>
        \nI'd like you to confirm whether you can see the content of the files.
        \nAre you familiar with the languages used in the project?
        \nNext, please detail the steps that would you take to take on the tasks that I just gave you. 
        \nIf you need more information, let me know, I'll be happy to provide.
        """ # the XML tags are best for Claude but it wouldn't to include for other AIs.
