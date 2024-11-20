import subprocess
from agents.base_agent import BaseAgent

class DebuggerAgent(BaseAgent):
    def debug_task(self, task_id, code_snippet):
        """Run and debug the provided code snippet."""
        # Add the task to short-term memory
        self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "in progress"})

        # Run the code snippet
        result = self.run_code(code_snippet)
        if result["status"] == "error":
            error_message = result["output"]
            fix = self.suggest_fix(error_message, code_snippet)
            # Update task memory with error and suggested fix
            self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "error", "fix": fix})
            return f"Error: {error_message}\nSuggested Fix: {fix}"
        else:
            # Mark the task as successful
            self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "success"})
            return "Task completed successfully."

    def suggest_fix(self, error_message, code_snippet):
        """Placeholder for suggesting fixes based on error messages."""
        # Example logic for generating a fix suggestion
        return "Check your data types or ensure all variables are defined."

    def run_code(self, code):
        """Run the provided code snippet and capture output/errors."""
        try:
            exec(code)  # This is for simplicity; sandboxing is safer for real use cases.
            return {"status": "success", "output": "Code ran successfully."}
        except Exception as e:
            return {"status": "error", "output": str(e)}
