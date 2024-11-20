import sqlite3

class MultiMemory:
    def __init__(self):
        self.task_memory = {}  # Short-term memory for current tasks
        self.init_code_memory()  # Initialize persistent code memory

    def init_code_memory(self):
        """Set up SQLite database for persistent memory."""
        self.conn = sqlite3.connect("memory/persistence/code_memory.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_memory (
                file_name TEXT PRIMARY KEY,
                code TEXT
            )
        """)
        self.conn.commit()

    def add_task_memory(self, task_id, data):
        """Store task-specific data in short-term memory."""
        self.task_memory[task_id] = data

    def get_task_memory(self, task_id):
        """Retrieve task-specific memory."""
        return self.task_memory.get(task_id)

    def add_code_memory(self, file_name, code):
        """Store or update a file's code in persistent memory."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO code_memory (file_name, code)
            VALUES (?, ?)
        """, (file_name, code))
        self.conn.commit()

    def get_code_memory(self, file_name):
        """Retrieve the code for a specific file."""
        self.cursor.execute("SELECT code FROM code_memory WHERE file_name = ?", (file_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def list_code_files(self):
        """List all files stored in persistent memory."""
        self.cursor.execute("SELECT file_name FROM code_memory")
        return [row[0] for row in self.cursor.fetchall()]
