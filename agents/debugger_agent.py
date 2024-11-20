import subprocess
from agents.base_agent import BaseAgent

class DebuggerAgent(BaseAgent):
    def debug_task(self, task_id, code_snippet):
        """Run and debug the provided code snippet."""
        # Check if the code needs to be chunked
        if len(code_snippet.splitlines()) > 50:  # Example threshold
            return self.debug_large_code(task_id, code_snippet)
        
        # Debug normally for smaller code
        return self.debug_single_chunk(task_id, code_snippet)

    def debug_single_chunk(self, task_id, code_snippet):
        """Debug a single chunk of code."""
        self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "in progress"})
        self.memory.add_code_memory(f"{task_id}.py", code_snippet)

        result = self.run_code(code_snippet)
        if result["status"] == "error":
            error_message = result["output"]
            fix = self.suggest_fix(error_message, code_snippet)
            self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "error", "fix": fix})
            return f"Error: {error_message}\nSuggested Fix: {fix}"
        else:
            self.memory.add_task_memory(task_id, {"code": code_snippet, "status": "success"})
            return "Task completed successfully."

    def debug_large_code(self, task_id, code_snippet):
        """Break large code into chunks and debug each chunk."""
        lines = code_snippet.splitlines()
        chunk_size = 50  # Number of lines per chunk
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

        print(f"Debugging large code ({len(chunks)} chunks):")
        results = []

        for idx, chunk in enumerate(chunks):
            chunk_task_id = f"{task_id}_chunk_{idx}"
            chunk_code = "\n".join(chunk)
            print(f"Processing chunk {idx + 1}/{len(chunks)}")
            result = self.debug_single_chunk(chunk_task_id, chunk_code)
            results.append(result)
        
        # Aggregate results
        summary = "\n".join(results)
        return f"Large Code Debugging Summary:\n{summary}"

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
