# AutoCoder

AutoCoder is an AI-powered coding assistant built with a multi-memory architecture. It is designed to debug, write, and manage code autonomously. This project focuses on creating a custom, local AI agent system that can solve complex programming tasks with both short-term and persistent memory.

---

## **Getting Started**

Follow these steps to set up and run AutoCoder on your machine.

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/AutoCoder.git
cd AutoCoder
```

### **2. Set Up a Virtual Environment**
Create and activate a Python virtual environment to manage dependencies:
```bash
python -m venv venv
```

#### • For Linux/Mac:
```bash
source venv/bin/activate
```

#### • For Windows:
```bash
venv\Scripts\activate
```

### **3. Install Dependencies**
Use the 'requirements.txt' file to install all required libraries:
```bash
pip install -r requirements.txt
```

### **4. Install LLM's**
You'll need to download some LLm's that take a while to download, there large files.

#### Edit '_cred.py' file in root of 'AutoCoder/'
Read everything in that file, then once everything is filled out, rename the file too 'cred.py'

#### Now run Coder agent so we can download the LLM it uses.
This will take a while to download.
```bash
python agents/coder_agent.py
```

### **5. Run the Program**
To run the main entry point for AutoCoder:
```bash
python main.py
```

---

## **Project Structure**
```bash
AutoCoder/
├── main.py                 # Entry point for the project
├── agents/                 # Folder for agent classes
│   ├── __init__.py         # Makes this a Python package
│   ├── base_agent.py       # Base agent class (shared logic)
│   ├── debugger_agent.py   # Debugger-specific implementation
│   ├── coder_agent.py      # Code-specific implementation
├── models/                 # Folder for LLM's
│   ├── starcoder/          # Folder for StarCoder model files
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
```

---

### Contriuting
Contributions are welcome! Feel free to open issues or submit pull requests.

---

### License
This project is licensed under the MIT License.