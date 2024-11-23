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
├── .git/
├── __pycache__/
├── agents/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── coder_agent.py
│   └── debugger_agent.py
├── datasets/
│   └── errors_and_fixes.json
├── logs/
│   └── debug.log
├── memory/
│   ├── __pycache__/
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── code_memory.db
│   ├── __init__.py
│   └── multi_memory.py
├── models/
│   ├── some_model/
│   └── starcoder/
│       ├── .locks/
│       │   └── models--bigcode--starcoder/
│       └── models--bigcode--starcoder/
│           ├── .no_exist/
│           │   └── 827cd7721231872c152e3faef5cae1b22964ed58/
│           │       ├── added_tokens.json
│           │       └── model.safetensors
│           ├── blobs/
│           ├── refs/
│           │   └── main
│           └── snapshots/
│               └── 827cd7721231872c152e3faef5cae1b22964ed58/
│                   ├── config.json
│                   ├── merges.txt
│                   ├── model-00001-of-00007.safetensors
│                   ├── model-00002-of-00007.safetensors
│                   ├── model-00003-of-00007.safetensors
│                   ├── model-00004-of-00007.safetensors
│                   ├── model-00005-of-00007.safetensors
│                   ├── model-00006-of-00007.safetensors
│                   ├── model-00007-of-00007.safetensors
│                   ├── model.safetensors.index.json
│                   ├── special_tokens_map.json
│                   ├── tokenizer.json
│                   ├── tokenizer_config.json
│                   └── vocab.json
├── tests/
│   ├── test_agents.py
│   ├── test_memory.py
│   └── test_tools.py
├── tools/
│   ├── __init__.py
│   ├── code_runner.py
│   ├── error_parser.py
│   └── task_utils.py
├── venv/
├── .gitignore
├── README.md
├── _cred.py
├── clear_cache.py
├── cred.py
├── generate_structure.py
├── main.py
├── notes.md
└── requirements.txt
```

---

### Contriuting
Contributions are welcome! Feel free to open issues or submit pull requests.

---

### License
This project is licensed under the MIT License.