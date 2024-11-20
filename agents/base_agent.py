class BaseAgent:
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory

    def log(self, message):
        """Log activity of the agent."""
        print(f"[{self.name}] {message}")
