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
                                 f"Please note that you will not be able to directly interact with the files. You can only suggest changes to be made by sending code snippets to the user." \
                                 f"Only provide the new code snippets or relevant code sections to update in order to save token usage." \
                                 f"Use a git diff notation to show what is new, what is replaced, what is deleted." \
                                 f"Do not show what hasn't changed."

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
        \nStep 1: First make sure that you understand what is required from the tasks. 
        Propose a plan with specific steps and milestones.
        Stop and wait for user's feedbacks on your proposed plan.
        \nStep 2: With the user's feedbacks on the plan, update the proposed plan if necessary. 
        If user approves of the plan, start moving through the proposed plan incrementally and output required code chunks. 
        Remember, you can't edit on the files themselves so you will always have to rely on the user to create/update the files in the project.
        Stop and wait for user's feedbacks at each step.
        Update itiratively your previous thoughts, outputs accordingly.
        Once the user approves of the outputs for the step, the user will take your code and try to merge it into existing code. 
        Do whatever you can to make the process as smooth as possible.
        Ask if the users have finished implementing the new codes. Once the the user confirms that he/she is done, move on to the next step.
        \nStep 3: Once you have covered all steps in the plan, summarise what has been done, discussed. 
        Include all the relevant revisions and feedbacks.
        """ # the XML tags are best for Claude but it wouldn't to include for other AIs.
