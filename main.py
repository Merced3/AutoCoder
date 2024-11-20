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
    print("Hello" + name)
greet(123)
"""

    print("Starting Debug Task...")
    result = agent.debug_task("task_1", code_snippet)
    print(result)

if __name__ == "__main__":
    main()
