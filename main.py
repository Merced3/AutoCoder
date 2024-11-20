from agents.debugger_agent import DebuggerAgent
from memory.multi_memory import MultiMemory

def main():
    # Initialize the multi-memory system
    memory = MultiMemory()

    # Initialize the Debugger Agent
    agent = DebuggerAgent("Debugger1", memory)

    # Define the project structure
    project_structure = """
AutoCoder/
├── main.py                 # Entry point for the project
├── agents/                 # Folder for agent classes
│   ├── __init__.py         # Makes this a Python package
│   ├── base_agent.py       # Base agent class (shared logic)
│   ├── debugger_agent.py   # Debugger-specific implementation
├── memory/                 # Folder for memory system
│   ├── __init__.py         # Makes this a Python package
│   ├── multi_memory.py     # Multi-memory class implementation
│   ├── persistence/        # Folder for persistent storage
│       ├── __init__.py     # Package for persistent memory
│       ├── code_memory.db  # SQLite database for persistent code memory
├── tools/                  # Tools for debugging, testing, etc.
│   ├── __init__.py         # Package for utility tools
│   ├── code_runner.py      # Executes code snippets safely
│   ├── error_parser.py     # Parses error messages
│   ├── task_utils.py       # Helper functions for task management
├── datasets/               # Folder for datasets (if training later)
│   ├── errors_and_fixes.json  # Example dataset for debugging
├── logs/                   # Folder for logs
│   ├── debug.log           # Log file for debugging outputs
├── tests/                  # Unit tests for everything
│   ├── test_memory.py      # Tests for the memory system
│   ├── test_agents.py      # Tests for the agents
│   ├── test_tools.py       # Tests for utility tools
├── requirements.txt        # Python dependencies
├── README.md               # Project description
"""
    # Store the project structure in memory
    memory.set_project_structure(project_structure)

    # Example code snippet with an intentional bug (large code example)
    code_snippet = """
def greet(name):
    print("Hello " + name)

def add_numbers(a, b):
    return a + b

for i in range(100):  # Simulate repetitive logic for large code
    print(add_numbers(i, "test"))
""" * 10  # Repeat to simulate a large file

    # Debug the large code snippet
    print("Starting Debug Task...")
    result = agent.debug_task("task_1", code_snippet)
    print(result)

    # Visualize the memory contents
    print("\nVisualizing Memory:")
    memory.visualize_memory()

    # Export the current project memory
    memory.export_project("AutoCoder")

    # Clear the memory for a new project
    memory.clear_project()

if __name__ == "__main__":
    main()