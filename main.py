from agents.debugger_agent import DebuggerAgent
from memory.multi_memory import MultiMemory

def main():
    # Initialize the multi-memory system
    memory = MultiMemory()

    # Initialize the Debugger Agent
    agent = DebuggerAgent("Debugger1", memory)

    # Example code snippet with an intentional bug
    code_snippet = """
def greet(name):
    print("Hello " + name)

def add_numbers(a, b):
    return a + b

for i in range(100):  # Simulate repetitive logic for large code
    print(add_numbers(i, "test"))
""" * 10  # Repeat to simulate a large file

    print("Starting Debug Task...")
    result = agent.debug_task("task_1", code_snippet)
    print(result)

    # Visualize the memory contents
    print("\nVisualizing Memory:")
    memory.visualize_memory()

if __name__ == "__main__":
    main()
