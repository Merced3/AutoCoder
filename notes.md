# Next steps:

### 1) Perfect the 'debugger_agent'
**• Model:** Not sure yet
**• Responsibility:** Validates the code, suggests fixes, and ensures functionality.
**• Task 1:** Debug Larger Pieces of Code.
    • This task will focus on integrating feedback from the **coder_agent** once it generates code.
    • Trial and error expected during implementation.
---
### 2) Perfect the 'coder_agent'
**• Model:** 
**• Responsibility:** Focuses on generating code for specific tasks based on the Coordinator's instructions.
**Tasks:** 
    • Download StarCoder, URL: https://huggingface.co/bigcode/starcoder
    • pip install transformers, DONE.
    • Create the following: 'models/starcoder/' and 'coder_agent.py', DONE.
    • Expand Coder Functionality:
        • Ensure it can generate all types of code (Python, JavaScript, SQL, etc.).
        • Add logic to identify and handle specific programming languages.
    • Integrate with Debugger: Once complete, move to the Debugger Agent to validate outputs.
---
### 3) Make the 'coordinator_agent'
**• Model:** gemini-1.5-flash-002, It excels at managing multi-step workflows. It can reliably call tools like the Coder and Debugger agents in sequence.
**• Responsibility:**
    • Acts as the Manager and Program Concepts Specialist.
    • Oversees project workflow.
    • Defines the project structure and creates/manages a **to-do list.**
    • Monitors progress and ensures agents stay aligned with project goals.
    • Prevents agents from deviating or getting stuck in rabbit holes.
    • Ensures modular, organized project structures.
**• Tasks:**
    • Download Gemini-1.5-flash-002:
        • Source: TBD. Research and validate availability for download and offline usage.
    • Plan Implementation:
        • Design how the Coordinator Agent will interface with the Coder and Debugger.





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










How to type messages for markdown compatible editors so i don't forget:
# Title
## Subtitle
### Section

horizontal Line: 
---

Bold Text **Here**

**For Code Blocks:**
```
code...
```

**For terminal output:**
```bash
Some terminal output message...
```
