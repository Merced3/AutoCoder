import sqlite3
import os
import shutil

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

    def visualize_memory(self):
        """Visualize the memory contents."""
        print("\nTask Memory:")
        if not self.task_memory:
            print("No task memory available.")
        else:
            for task_id, data in self.task_memory.items():
                print(f"Task ID: {task_id}, Data: {data}")
        
        print("\nCode Memory:")
        code_files = self.list_code_files()
        if not code_files:
            print("No code memory available.")
        else:
            for file_name in code_files:
                code = self.get_code_memory(file_name)
                print(f"File: {file_name}\nCode:\n{code}\n")

    def set_project_structure(self, structure):
        """Save the directory structure of the project."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO code_memory (file_name, code)
            VALUES ('project_structure', ?)
        """, (structure,))
        self.conn.commit()

    def get_project_structure(self):
        """Retrieve the directory structure of the project."""
        self.cursor.execute("SELECT code FROM code_memory WHERE file_name = 'project_structure'")
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def export_project(self, project_name):
        """Export the current project memory to a file."""
        export_path = f"{project_name}_code_memory.db"
        shutil.copyfile("memory/persistence/code_memory.db", export_path)
        print(f"Project exported to {export_path}")

    def clear_project(self):
        """Clear all project data from memory."""
        self.cursor.execute("DELETE FROM code_memory")  # Clear all rows
        self.conn.commit()  # Ensure changes are committed to the database
        self.cursor.execute("VACUUM")  # Reorganize the database to reclaim disk space
        print("Code memory cleared for new project.")