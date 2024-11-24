from openai import OpenAI
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("CODER_ASSISTANT_ID")
DATASET_PATH = "./datasets"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CoderAgent:
    def __init__(self, assistant_id, dataset_path=DATASET_PATH):
        print("Initializing CoderAgent...")
        self.assistant_id = assistant_id
        self.dataset_path = dataset_path
        self.files_folder = f"{dataset_path}/coder_files"

        # Ensure folders exist
        os.makedirs(self.files_folder, exist_ok=True)
        print(f"Ensured file folder exists: {self.files_folder}")

    def handle_required_action(self, thread_id, run_id, required_action):
        try:
            if required_action.type == "submit_tool_outputs":
                # Get the tool call details
                tool_call = required_action.submit_tool_outputs.tool_calls[0]

                # Dynamically generate tool output
                tool_output = {}
                if tool_call.function.name == "get_code":
                    tool_arguments = json.loads(tool_call.function.arguments)
                    # Example output for `get_code`
                    tool_output = {
                        "success": "true",
                        "code": f"# {tool_arguments['script_description']}\ndef fibonacci(): pass"
                    }
                else:
                    print(f"Unknown tool function: {tool_call.function.name}")
                    return None

                # Convert tool_output to a JSON string
                tool_output_json = json.dumps(tool_output)

                # Submit the tool output
                response = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run_id,
                    tool_outputs=[
                        {
                            "tool_call_id": tool_call.id,
                            "output": tool_output_json  # Pass as JSON string
                        }
                    ]
                )
                print(f"Tool outputs submitted successfully!")
                return response
            else:
                print("No submit_tool_outputs action required.")
        except Exception as e:
            print(f"Error handling required action: {e}")
            return None

    def create_thread(self, content):
        try:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            print(f"Thread created: {thread.id}")

            # Submit the thread to the assistant, as a new run.
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant_id)
            print(f"RUN Created: {run.id}")

            # Wait for run to complete
            while run.status not in ["completed", "failed"]:
                if run.status == "requires_action":
                    print(f"Run requires action: {run.required_action.type}, Tool Calls: {len(run.required_action.submit_tool_outputs.tool_calls)}")
                    action_result = self.handle_required_action(thread_id=thread.id, run_id=run.id, required_action=run.required_action)
                    if not action_result:
                        print("Action handling failed, aborting.")
                        break
                else:
                    print(f"Run Status: {run.status}")

                # Refresh the run status
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status == "completed":
                print("Run Completed!")
            else:
                print("Run failed or could not be completed.")

            return thread.id, run.id
        except Exception as e:
            print(f"Failed to create thread: {e}")
            return None  

    def get_response(self, thread_id):
        try:
            message_response = client.beta.threads.messages.list(thread_id)
            messages = message_response.data
            latest_message = messages[0]

            # Extract the raw content
            raw_content = latest_message.content[0].text.value
            print(f"\n Raw Content:\n{raw_content}\n")
            
            # Normalize and clean content
            raw_content = raw_content.strip()  # Strip any leading/trailing spaces
            if raw_content.startswith("```") and raw_content.endswith("```"):
                print("Starts and ends with ```/``` - cleaning it.")
                cleaned_content = raw_content[3:-3].strip()  # Remove outer backticks
                if "\n" in cleaned_content:  # Check for a potential language identifier
                    first_line, remaining_content = cleaned_content.split("\n", 1)
                    if first_line.strip().isalpha():  # If the first line looks like a language hint
                        cleaned_content = remaining_content.strip()  # Remove the language hint
            else:
                cleaned_content = raw_content  # No backticks, use as-is

            # Print the cleaned response for verification
            print(f"\nCleaned Response:\n{cleaned_content}")
            return cleaned_content
        except Exception as e:
            print(f"\nError during message retrieval: {e}")
            return None

    def save_to_dataset(self, action, file_name, script_description, script_code):
        print("Saving response to dataset...")
        dataset_file = f"{self.dataset_path}/coder_dataset.json"

        # Save the generated response to a file
        try:
            file_path = os.path.join(self.files_folder, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as code_file:
                code_file.write(script_code)

            print(f"Generated code saved to: {file_path}")

            # Load or initialize the dataset
            if os.path.exists(dataset_file):
                with open(dataset_file, "r", encoding="utf-8") as file:
                    try:
                        dataset = json.load(file)
                    except json.JSONDecodeError:
                        print("Invalid JSON format in dataset. Reinitializing...")
                        dataset = []
            else:
                dataset = []

            # Add metadata about the generated file
            new_entry = {
                "task": action,
                "file_name": file_name,
                "prompt": script_description,
                "output_path": file_path
            }
            dataset.append(new_entry)

            # Save updated metadata back to the dataset file
            with open(dataset_file, "w", encoding="utf-8") as file:
                json.dump(dataset, file, indent=4, ensure_ascii=False)

            print("Response metadata saved successfully.")
        except Exception as e:
            print(f"Error saving to dataset: {e}")


if __name__ == "__main__":
    # Validate API Key and Assistant ID
    if not OPENAI_API_KEY or not ASSISTANT_ID:
        raise ValueError("Missing API key or assistant ID in environment variables. Check .env file.")

    # Create an instance of the agent
    coder_agent = CoderAgent(assistant_id=ASSISTANT_ID)

    action = "create"
    file_name = "calculator.py"
    script_description = "A Python script that performs basic arithmetic operations (addition, subtraction, multiplication, division)."
    content = f"{action}, {file_name}, {script_description}"

    thread_id, run_id = coder_agent.create_thread(content)
    if thread_id and run_id:
        code = coder_agent.get_response(thread_id)
        if code:
            coder_agent.save_to_dataset(action, file_name, script_description, code)
