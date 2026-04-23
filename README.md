# 🤖 AI Data Analyst Agent

A simple yet powerful autonomous agent that uses artificial intelligence to analyze data and answer questions about datasets. The agent thinks through problems step-by-step, writes and executes Python code, and provides intelligent answers — all without human intervention.

**Perfect for learning:** How AI agents work, how to build intelligent applications, and how to create data analysis automation.

---

## 📋 Table of Contents

1. [How It Works (Plain English)](#how-it-works-plain-english)
2. [Architecture Overview](#architecture-overview)
3. [Project Structure](#project-structure)
4. [Component Explanation](#component-explanation)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
7. [Extending with Custom Data Files](#extending-with-custom-data-files)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)

---

## 🧠 How It Works (Plain English)

### The Agent's Thought Process

When you ask the agent a question like **"What is the average salary?"**, here's what happens internally:

1. **You Ask a Question** → You type your question into the terminal
2. **Agent Thinks** → The LLM (Large Language Model) receives your question and thinks about how to answer it
3. **Agent Decides** → The agent picks an action: either "write Python code to analyze" or "give a direct answer"
4. **Agent Acts** → If code is needed, the agent writes and runs Python code to analyze the data
5. **Agent Observes** → The agent sees the results and stores them in memory
6. **Agent Learns** → If more analysis is needed, it uses the previous results to make the next decision
7. **Agent Answers** → Once it has enough information, it provides the final answer

### The Agent's Internal Loop (Repeat up to 5 times)

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  1. LLM thinks about the question              │
│  2. LLM creates a "Thought" explaining why     │
│  3. LLM decides on an "Action"                 │
│     - python_code: Write analysis code         │
│     - final_answer: Give the answer            │
│                                                 │
│  IF python_code:                               │
│    → Agent runs the code                       │
│    → Stores result in memory                   │
│    → Asks next question based on result        │
│                                                 │
│  IF final_answer:                              │
│    → Agent returns answer to you               │
│    → Loop ends, done!                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Example Conversation Flow

```
User: "What is the average salary?"

Step 1:
- Thought: "I need to load the CSV file and calculate average salary"
- Action: python_code
- Code: df = pd.read_csv('data/sample.csv')
         avg = df['salary'].mean()
- Result: 70000.0

Step 2:
- Thought: "I have the average salary, I can now give the final answer"
- Action: final_answer
- Answer: "The average salary is $70,000"

Done! ✅
```

---

## 🏗️ Architecture Overview

### High-Level System Design

```
┌──────────────────────────────────────────────────────────────┐
│                        USER INPUT                             │
│                    (Terminal Question)                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    MAIN ENTRY POINT                           │
│                   (app/main.py)                              │
│  - Accepts user questions                                   │
│  - Creates the Agent                                        │
│  - Displays answers                                         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   SINGLE AGENT LOOP                           │
│              (app/agent/agent.py)                            │
│                                                              │
│  For each iteration (max 5):                                │
│  1. Build prompt with question + memory                    │
│  2. Send to LLM via provider                              │
│  3. Parse response (thought, action, code)                │
│  4. Execute action (code or final answer)                 │
│  5. Store result in memory                                │
│  6. Continue if needed                                    │
└──────┬───────────────────────┬──────────────┬───────────────┘
       │                       │              │
       ▼                       ▼              ▼
   ┌────────────────┐  ┌──────────────┐  ┌─────────────┐
   │  LLM Provider  │  │ Parser       │  │  Python     │
   │  Selection     │  │ & Extraction │  │  Executor   │
   │                │  │              │  │             │
   │ (OpenAI or     │  │ Regex parse  │  │ Runs code   │
   │  Groq API)     │  │ LLM output   │  │ in sandbox  │
   │                │  │ for:         │  │ maintains  │
   └────────────────┘  │              │  │ state      │
                       │ - thought    │  │             │
                       │ - action     │  └─────────────┘
                       │ - code       │
                       │ - answer     │
                       └──────────────┘
                            │
                            ▼
                      ┌─────────────────┐
                      │  Memory Buffer  │
                      │                 │
                      │ Stores last 5   │
                      │ interactions    │
                      │ for context     │
                      └─────────────────┘
```

---

## 📁 Project Structure

```
ai-data-analyst/
│
├── 📄 README.md                          # This documentation
├── 📄 pyproject.toml                     # Project dependencies
├── 📄 .env                               # Configuration (API keys)
│
├── 📂 app/                               # Main application code
│   ├── main.py                           # Entry point - user talks to agent here
│   │
│   ├── agent/                            # The Agent's Brain
│   │   ├── agent.py                      # Main agent loop (decision-making)
│   │   ├── prompt.py                     # Creates instructions for LLM
│   │   └── parser.py                     # Extracts thought/action from LLM output
│   │
│   ├── models/                           # Provider Selection & Execution
│   │   ├── base.py                       # Abstract interface for any LLM
│   │   ├── openai_client.py              # OpenAI connection & API calls
│   │   ├── groq_client.py                # Groq connection & API calls
│   │   ├── factory.py                    # Switches between providers
│   │   └── llm.py                        # Backward compatibility
│   │
│   ├── tools/                            # Code Execution & Data Tools
│   │   ├── python_executor.py            # Runs Python code safely
│   │   └── file_tool.py                  # File operations (for future)
│   │
│   ├── memory/                           # Agent's Short-Term Memory
│   │   └── buffer.py                     # Stores recent analysis steps
│   │
│   ├── core/                             # Core Configuration & Logging
│   │   ├── config.py                     # Settings & API keys
│   │   └── logger.py                     # Logging setup
│   │
│   └── schemas/                          # Data Structures
│       └── agent_schema.py               # Response format definition
│
├── 📂 data/                              # Data Files
│   └── sample.csv                        # Sample employee data
│
├── 📂 scripts/                           # Utility Scripts
│   └── run_agent.sh                      # Quick start script
│
└── 📂 tests/                             # Unit Tests
    ├── test_agent.py                     # Test agent behavior
    └── test_tool.py                      # Test code execution
```

---

## 🔍 Component Explanation

### 1. **Entry Point** (`app/main.py`)
**What it does:** This is where users interact with the agent.

```python
# Simple loop that:
# 1. Asks user for a question
# 2. Creates an agent
# 3. Runs the agent with the question
# 4. Prints the answer
# 5. Repeats until user types "exit"
```

**In Plain English:** Think of it as a chatbot interface. You type questions, and answers come back.

---

### 2. **The Agent Brain** (`app/agent/agent.py`)
**What it does:** The core decision-making engine that runs the think-act-observe loop.

**How it works:**
- Takes your question
- Builds a prompt with instructions and previous memory
- Sends to the LLM (AI model)
- Parses the response to extract `thought`, `action`, and `code`
- Executes the action (run code OR give final answer)
- Stores result in memory
- Repeats up to 5 times

**In Plain English:** This is the agent's brain. It decides what to do and coordinates everything.

---

### 3. **Prompt Builder** (`app/agent/prompt.py`)
**What it does:** Creates the instructions that tell the AI model what to do.

**Key instructions given to the LLM:**
- You are a data analyst
- Your data is in `data/sample.csv`
- You can write Python code
- Format your response as: `Thought: ... Action: ... Code/Answer: ...`
- Pandas is available as `pd`
- Variables persist between code runs

**In Plain English:** This is like giving your AI assistant a detailed job description and rules to follow. Better instructions = better responses.

---

### 4. **Response Parser** (`app/agent/parser.py`)
**What it does:** Reads the LLM's response and extracts the key information.

**Extractions it performs:**
```
Raw LLM Output:
"Thought: I need to load the data
Action: python_code
```python
df = pd.read_csv('data/sample.csv')
result = df['salary'].mean()
```"

↓ Parser extracts ↓

thought: "I need to load the data"
action: "python_code"
code: "df = pd.read_csv(...)\nresult = df['salary'].mean()"
```

**In Plain English:** The LLM's response is messy text. The parser extracts the clean, structured parts we need.

---

### 5. **LLM Provider System** (`app/models/`)
**What it does:** Flexible system to switch between different AI models.

**Architecture:**
- `base.py` - Defines the interface (contract) that all providers must follow
- `openai_client.py` - Connects to OpenAI's GPT models
- `groq_client.py` - Connects to Groq's models (faster, cheaper)
- `factory.py` - Chooses which provider to use based on `.env` configuration

**In Plain English:** Instead of hardcoding one AI model, we built a flexible system where you can easily switch providers. Want to try Groq instead of OpenAI? Just change the config!

**Example usage:**
```bash
# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# OR use Groq (faster & cheaper)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk-...
```

---

### 6. **Python Code Executor** (`app/tools/python_executor.py`)
**What it does:** Safely runs Python code written by the AI.

**Key features:**
- Maintains **persistent state** - Variables created in one code run are available in the next
- Pre-imports pandas as `pd` automatically
- Catches errors and returns them as text
- Prevents dangerous operations (sandboxed execution)

**Example:**
```python
# First execution
execute_python("df = pd.read_csv('data/sample.csv')")

# Second execution - df is STILL available!
execute_python("print(df['salary'].mean())")  # Works! df exists
```

**In Plain English:** This is the sandbox where the AI's code runs. It's designed so the AI can use variables from previous steps.

---

### 7. **Memory Buffer** (`app/memory/buffer.py`)
**What it does:** Stores the last 5 interactions so the agent remembers context.

**How it works:**
```python
# Step 1: Question asked
memory.add("User asked: What is average salary?")

# Step 2: First analysis
memory.add("Loaded CSV, found average = 70000")

# Step 3: Agent remembers previous steps
context = memory.get_context()  # Returns last 5 items
# Now LLM knows what happened before!
```

**In Plain English:** Without memory, the agent would repeat the same analysis. With memory, it knows what already happened and can build on it.

---

### 8. **Configuration** (`app/core/config.py`)
**What it does:** Central place for all settings.

**Settings include:**
- Which LLM provider (OpenAI or Groq)
- API keys for each provider
- Model names
- Maximum steps (5)
- Token limits

**In Plain English:** This is the settings dashboard. Change something here, and the whole app adapts.

---

### 9. **Logging** (`app/core/logger.py`)
**What it does:** Tracks what the agent is doing (for debugging and understanding).

**Output example:**
```
2026-04-23 06:50:52 | INFO | app.models.factory | Initializing Groq client
2026-04-23 06:50:52 | INFO | app.agent.agent | 🧠 Thought: I need to load the data
2026-04-23 06:50:52 | INFO | app.agent.agent | ⚙️ Action: python_code
2026-04-23 06:52:05 | INFO | app.agent.agent | 📊 Observation: average salary = 70000
```

**In Plain English:** These are detailed notes showing what the agent is thinking and doing. Helpful for debugging.

---

### 10. **Data Schema** (`app/schemas/agent_schema.py`)
**What it does:** Defines the structure of the agent's response.

```python
class AgentResponse:
    thought: str              # What the AI was thinking
    action: str              # What to do (python_code or final_answer)
    code: Optional[str]      # Python code to run (if action=python_code)
    final_answer: Optional[str]  # Answer to give user (if action=final_answer)
```

**In Plain English:** This ensures every response has the right structure. It's a contract/promise about what data will be returned.

---

## ✅ Installation & Setup

### Step 1: Prerequisites
- Python 3.13+
- An API key from **OpenAI** or **Groq** (or both)

### Step 2: Install the Project

```bash
# Navigate to the project
cd ai-data-analyst

# Install dependencies
# Option A: Using uv (recommended, faster)
uv sync

# Option B: Using traditional pip
pip install -e .
```

### Step 3: Configure API Keys

Create a `.env` file in the project root:

```bash
# Choose your LLM provider
LLM_PROVIDER=openai       # or "groq"

# OpenAI configuration
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini

# Groq configuration (optional)
GROQ_API_KEY=gsk-your-actual-key-here
GROQ_MODEL=mixtral-8x7b-32768

# Agent settings
MAX_STEPS=5                # Max iterations for analysis
```

### Step 4: Verify Installation

```bash
# Test if everything works
python -c "from app.agent.agent import SingleAgent; print('✅ Installation successful!')"
```

---

## 🚀 Usage Guide

### Basic Usage

```bash
# Start the agent
uv run python app/main.py

# In the terminal, ask questions:
Ask: What is the average salary?
Ask: What are the salary statistics?
Ask: exit   # Type 'exit' to quit
```

### Example Queries and Responses

**Query 1: Simple calculation**
```
Ask: What is the average salary?

✅ Final Answer: The average salary is $70,000
```

**Query 2: More complex analysis**
```
Ask: Show me salary by age group

✅ Final Answer: 
- Ages 20-30: $60,000 average
- Ages 30-40: $80,000 average
- Ages 40+: $90,000 average
```

### How to Read the Logs

When you run the agent, you'll see detailed logs:

```
2026-04-23 06:50:52 | INFO | app.models.factory | Initializing Groq client
```
→ The agent chose Groq as its LLM provider

```
2026-04-23 06:50:52 | INFO | app.agent.agent | 🧠 Thought: I need to load the CSV and calculate average
```
→ The agent is thinking about what to do

```
2026-04-23 06:50:52 | INFO | app.agent.agent | ⚙️ Action: python_code
```
→ The agent decided to execute Python code

```
2026-04-23 06:52:05 | INFO | app.agent.agent | 📊 Observation: average = 70000
```
→ The code ran successfully and produced this result

---

## 🔧 Extending with Custom Data Files

### The Problem
Currently, the agent only analyzes `data/sample.csv`. To make it truly flexible, we need to let users provide their own CSV or Excel files.

### Solution Architecture

Let's update the system to support user-provided files:

#### Step 1: Update the Prompt Builder

```python
# In app/agent/prompt.py
def build_prompt(user_input: str, memory: str, data_file: str = "data/sample.csv") -> str:
    """Now accepts a custom data file path"""
    return f"""
    You can load data with: df = pd.read_csv('{data_file}')
    ...rest of prompt
    """
```

#### Step 2: Create a Data Manager

Create a new file `app/tools/data_manager.py`:

```python
import os
import pandas as pd
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class DataManager:
    """Manages data file loading and validation"""
    
    def __init__(self, default_file: str = "data/sample.csv"):
        self.current_file = default_file
        self.data_info = self._get_file_info()
    
    def _get_file_info(self):
        """Get information about the current data file"""
        try:
            if self.current_file.endswith('.csv'):
                df = pd.read_csv(self.current_file)
            elif self.current_file.endswith('.xlsx'):
                df = pd.read_excel(self.current_file)
            else:
                raise ValueError("Only CSV and Excel files supported")
            
            return {
                "file": self.current_file,
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict()
            }
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
    
    def load_file(self, file_path: str):
        """Load a new data file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.current_file = file_path
        self.data_info = self._get_file_info()
        logger.info(f"Loaded file: {file_path}")
        logger.info(f"Rows: {self.data_info['rows']}, Columns: {self.data_info['columns']}")
    
    def get_info_text(self):
        """Get human-readable info about the data"""
        return f"File: {self.data_info['file']}\nRows: {self.data_info['rows']}\nColumns: {', '.join(self.data_info['columns'])}"
```

#### Step 3: Update the Main Entry Point

```python
# In app/main.py
from app.tools.data_manager import DataManager

def main():
    agent = SingleAgent()
    data_manager = DataManager()
    
    print("📊 AI Data Analyst Agent")
    print(f"Current data: {data_manager.get_info_text()}\n")
    
    while True:
        command = input("\nAsk (or type 'load <file OR 'exit'): ").strip()
        
        if command.lower() == "exit":
            break
        elif command.lower().startswith("load "):
            file_path = command[5:].strip()
            try:
                data_manager.load_file(file_path)
                print(f"✅ Loaded: {data_manager.get_info_text()}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            # Pass the data file to the agent
            agent.current_data_file = data_manager.current_file
            answer = agent.run(command)
            print(f"\n✅ Final Answer: {answer}")
```

#### Step 4: Update Agent to Use Custom File

```python
# In app/agent/agent.py
class SingleAgent:
    def __init__(self):
        self.llm = create_llm_client()
        self.memory = MemoryBuffer()
        self.current_data_file = "data/sample.csv"  # Default file
        reset_execution_env()
    
    def run(self, user_input: str):
        for step in range(settings.MAX_STEPS):
            # Pass custom file to prompt
            prompt = build_prompt(user_input, self.memory.get_context(), self.current_data_file)
            ...
```

### Usage Example with Custom Files

```bash
# Start the agent
uv run python app/main.py

ask (or type 'load <file>' OR 'exit'): load /path/to/your/file.csv
✅ Loaded: File: /path/to/your/file.csv, Rows: 1000, Columns: name, age, salary, department

Ask: What is the average salary?
✅ Final Answer: The average salary is $75,000

ask: load /path/to/different/data.xlsx
✅ Loaded: File: /path/to/different/data.xlsx, Rows: 500, Columns: product, sales, date

Ask: What are total sales by product?
✅ Final Answer: Product X: $50,000, Product Y: $35,000
```

### Future Enhancements

1. **Database Support** - Connect to MySQL, PostgreSQL, etc.
```python
def load_from_database(self, connection_string, query):
    df = pd.read_sql(query, connection_string)
```

2. **API Support** - Fetch data from APIs
```python
def load_from_api(self, endpoint, params):
    df = pd.read_json(requests.get(endpoint, params).json())
```

3. **Multiple File Processing** - Analyze across multiple files
```python
def load_multiple_files(self, file_list):
    # Merge and analyze
```

4. **Data Validation** - Check data quality before analysis
```python
def validate_data(self):
    # Check for nulls, duplicates, etc.
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# LLM Provider Selection
LLM_PROVIDER=openai              # Options: "openai" or "groq"

# OpenAI Configuration
OPENAI_API_KEY=sk-...            # Get from https://platform.openai.com/api-keys
OPENAI_MODEL=gpt-4o-mini         # Model name

# Groq Configuration  
GROQ_API_KEY=gsk-...             # Get from https://console.groq.com/keys
GROQ_MODEL=mixtral-8x7b-32768    # Model name

# Agent Configuration
MAX_STEPS=5                       # Maximum iterations for analysis (1-10)
MAX_TOKENS=150                    # Max tokens per LLM response (50-4096)
```

### Configuration Priority
1. Environment variables (`.env` file)
2. Runtime configuration in `app/core/config.py`
3. Defaults in the code

### How to Change Settings

**Option 1: Modify `.env` file**
```bash
LLM_PROVIDER=groq
MAX_STEPS=10
```

**Option 2: Temporarily override in code**
```python
from app.core.config import settings
settings.LLM_PROVIDER = "openai"
settings.MAX_STEPS = 10
```

---

## 🐛 Troubleshooting

### Issue 1: "API key not found"
**Symptom:** `Error: OPENAI_API_KEY not found in environment`

**Solution:**
1. Check `.env` file exists in project root
2. Verify API key is correct and not expired
3. Reload environment: `source .env` (Linux/Mac) or let the app reload

```bash
# Verify key is set
echo $OPENAI_API_KEY
```

### Issue 2: "Cannot import name 'create_llm_client'"
**Symptom:** `ImportError: cannot import name 'create_llm_client' from 'app.models.factory'`

**Solution:**
1. Ensure all `__init__.py` files exist in `app/models/`
2. Verify the factory.py file is not empty
3. Reinstall: `uv sync` or `pip install -e .`

### Issue 3: "No code block found" warnings
**Symptom:** Multiple "Warning: Action was 'python_code' but no code block found"

**Solution:**
1. The parser couldn't extract code from LLM response
2. This usually means the LLM isn't following format - try better prompt
3. Or switch to a different model: Change `LLM_PROVIDER` in `.env`

### Issue 4: "NameError: name 'df' is not defined"
**Symptom:** Code runs fine in step 1, but step 2 says `df` doesn't exist

**Solution:**
- This was fixed! The executor now maintains persistent state
- If it still happens, ensure you're using latest `python_executor.py`
- Try: `uv sync` to reinstall

### Issue 5: Agent keeps looping without answering
**Symptom:** The agent runs 5 steps but never gives a final answer

**Solution:**
1. The LLM might not understand the format
2. Try switching providers: `LLM_PROVIDER=groq` or `LLM_PROVIDER=openai`
3. Increase `MAX_TOKENS`: `MAX_TOKENS=300` in `.env`
4. Check the logs for parsing errors

### Issue 6: "Rate limit exceeded" error
**Symptom:** Error after a few queries

**Solution:**
1. You've hit the API rate limit
2. Wait a few minutes before making more requests
3. Consider upgrading your API subscription
4. Or use Groq (has much higher free limits!)

### Debug Mode

To see detailed debug information:

1. Update `app/core/logger.py` to set level to DEBUG:
```python
def setup_logger(name: str = "ai-agent", level: str = "DEBUG") -> logging.Logger:
    log_level = getattr(logging, level.upper(), logging.DEBUG)  # Changed to DEBUG
```

2. Run with debug flag:
```bash
DEBUG=1 uv run python app/main.py
```

---

## 📚 Learning Path

### Beginner
1. Run the agent with sample data
2. Read the logs and understand the flow
3. Change the `.env` to try different LLM providers
4. Modify the prompt in `app/agent/prompt.py`

### Intermediate
1. Add new features to the Memory Buffer
2. Create new tools in `app/tools/`
3. Experiment with different model configurations
4. Build the Data Manager for custom files

### Advanced
1. Add database connectivity
2. Implement multi-agent collaboration
3. Build a web interface with FastAPI
4. Deploy to production with containerization

---

## 🤝 Contributing

Want to improve the agent? Here are some ideas:

1. **New Tools** - File operations, API calls, email sending
2. **Better Parsing** - More robust response extraction
3. **UI** - Web interface instead of terminal
4. **Optimizations** - Faster inference, fewer API calls
5. **Documentation** - More examples and tutorials

---

## 📖 Key Concepts Explained

### What is an Agent?
An agent is a program that:
- Takes goals/questions as input
- Decides what actions to take
- Executes actions
- Observes results
- Makes new decisions based on observations
- Repeats until goal is achieved

It's like a very smart robot that can think, plan, and act.

### What is an LLM?
A Large Language Model (LLM) is an AI that:
- Understands English and other languages
- Can write code
- Can reason through problems
- Can have conversations

Examples: ChatGPT (OpenAI), Claude (Anthropic), Mixtral (Groq)

### Why is Memory Important?
- Without memory, agent forgets what it already learned
- Memory lets agent build on previous steps
- Makes analysis more efficient and coherent

### What is Prompt Engineering?
Prompt engineering is the art of writing instructions to the AI so it does what you want:
- Good prompt → Good results
- Bad prompt → Confused AI

The agent uses a well-engineered prompt in `app/agent/prompt.py`

---

## 📞 Support & Resources

- **OpenAI Documentation**: https://platform.openai.com/docs
- **Groq Documentation**: https://console.groq.com/docs
- **Pandas Documentation**: https://pandas.pydata.org/docs
- **Python Documentation**: https://docs.python.org

---

## 📄 License

This project is open source and available for learning purposes.

---

## 🎯 Quick Reference

### Start the agent
```bash
uv run python app/main.py
```

### Install dependencies
```bash
uv sync
```

### Run tests
```bash
pytest tests/
```

### Change LLM provider
1. Edit `.env`
2. Set `LLM_PROVIDER=groq` or `LLM_PROVIDER=openai`

### Add API key
1. Edit `.env`
2. Add `GROQ_API_KEY=your-key-here` or `OPENAI_API_KEY=your-key-here`

### View detailed logs
1. Edit `app/core/logger.py`
2. Change `level="INFO"` to `level="DEBUG"`

---

**Happy analyzing! 🚀**
