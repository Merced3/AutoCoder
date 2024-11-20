from agents.debugger_agent import DebuggerAgent
from memory.multi_memory import MultiMemory

def main():
    # Initialize the multi-memory system
    memory = MultiMemory()

    # Initialize the Debugger Agent
    agent = DebuggerAgent("Debugger1", memory)

    project_name = "AutoCoder"

    # Define the project structure
    project_structure = f"""
{project_name}/
├── main.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── debugger_agent.py
├── memory/
│   ├── multi_memory.py
"""
    # Store the project structure in memory
    memory.set_project_structure(project_structure)

    # Example large code snippet
    file_name = "main.py"
    code_snippet = """
def greet(name):
    print("Hello " + name)

def add_numbers(a, b):
    return a + b

for i in range(1000):  # Simulate repetitive logic for large code
    print(add_numbers(i, "test"))
"""

    # Debug the file as a single unit
    print(f"Debugging {file_name}...")
    result = agent.debug_task("task_1", code_snippet, file_name)
    print(result)

    # Visualize the memory contents
    print("\nVisualizing Memory:")
    memory.visualize_memory()

    # Export and clear the project
    memory.export_project(project_name)
    memory.clear_project()

if __name__ == "__main__":
    main()
