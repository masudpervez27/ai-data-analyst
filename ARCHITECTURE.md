# Architecture Guide - AI Data Analyst Agent

This document provides a deep technical dive into the system architecture for developers and advanced users.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Design Patterns](#design-patterns)
3. [Data Flow](#data-flow)
4. [Component Interactions](#component-interactions)
5. [State Management](#state-management)
6. [Extension Points](#extension-points)

---

## System Overview

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                    (app/main.py)                             │
│              User Interface / CLI Interface                  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│                    ORCHESTRATION LAYER                        │
│                  (app/agent/agent.py)                        │
│    Manages the agent loop (think-act-observe cycle)          │
└─────┬──────────┬──────────┬──────────┬──────────┬────────────┘
      │          │          │          │          │
┌─────▼──┐  ┌───▼────┐  ┌──▼───┐  ┌──▼────┐  ┌──▼────┐
│ Prompt │  │ Parser │  │ Code │  │Memory │  │Config │
│Builder │  │        │  │Exec  │  │Buffer │  │ory    │
│        │  │        │  │      │  │       │  │       │
└────────┘  └────────┘  └──────┘  └───────┘  └───────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│                  LLM PROVIDER LAYER                           │
│            (app/models/) - Factory Pattern                   │
│    Abstracts different LLM providers (OpenAI, Groq)          │
└─────────┬──────────────────────────────┬──────────────────────┘
          │                              │
     ┌────▼────────┐          ┌──────────▼──────────┐
     │ OpenAI API  │          │   Groq API          │
     │ Client      │          │   Client            │
     └─────────────┘          └─────────────────────┘
          │                              │
          └───────────────┬──────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │   External LLM Services  │
            │   (OpenAI, Groq clouds)  │
            └──────────────────────────┘
```

---

## Design Patterns

### 1. Factory Pattern (LLM Provider Selection)

**Purpose:** Allow easy switching between different LLM providers without changing code.

**Implementation:**
```
app/models/
    ├── base.py           ← Defines interface (Abstract)
    ├── openai_client.py  ← OpenAI implementation
    ├── groq_client.py    ← Groq implementation
    └── factory.py        ← Factory that creates right instance
```

**Pattern Diagram:**
```
┌─────────────────┐
│ LLMProvider     │ (Abstract Base Class)
│ (interface)     │
└────────┬────────┘
         │ implements
    ┌────┴────────────────────────┐
    │                             │
┌───▼──────────┐        ┌────────▼────────┐
│ OpenAIClient │        │ GroqClient      │
│              │        │                 │
│ generate()   │        │ generate()      │
└──────────────┘        └─────────────────┘
         ▲                      ▲
         │                      │
         └──────────┬───────────┘
                    │
             ┌──────▼──────┐
             │  factory()  │
             │  creates    │
             │   right     │
             │  client     │
             └─────────────┘
```

**Benefit:** Add new providers (Claude, LLaMA, etc.) without modifying existing code.

### 2. Strategy Pattern (Action Execution)

**Purpose:** Different action types (python_code, final_answer) are handled as strategies.

**Implementation in agent.py:**
```python
if parsed.action == "python_code":
    # Strategy 1: Execute code
    result = execute_python(parsed.code)
elif parsed.action == "final_answer":
    # Strategy 2: Return answer directly
    return parsed.final_answer
```

### 3. State Pattern (Persistent Execution Environment)

**Purpose:** Maintain state across multiple code executions.

**Implementation in python_executor.py:**
```
┌────────────────────────────────────┐
│   _EXECUTION_ENV (Global Dict)     │
│                                    │
│ Step 1: df = pd.read_csv(...)     │
│         _EXECUTION_ENV['df'] ← df  │
│                                    │
│ Step 2: df['salary'].mean()        │
│         Access df from env         │
└────────────────────────────────────┘
```

### 4. Template Method Pattern (Agent Loop)

**Purpose:** Define the skeleton of the analysis algorithm.

**Implementation:**
```
Agent Loop Template:
1. Get user input
2. While not done (max 5 steps):
   a. Build prompt with memory
   b. Call LLM
   c. Parse response
   d. Execute action
   e. Store result in memory
   f. Check if final answer reached
```

---

## Data Flow

### Complete Request Journey

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER INPUT                                               │
│    "What is the average salary?"                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 2. PROMPT BUILDING (app/agent/prompt.py)                   │
│    + System instructions                                    │
│    + Memory context (previous steps)                        │
│    + Data file info                                         │
│    + User question                                          │
│    ▼                                                         │
│    "You are a data analyst. Available: df = pd.read_csv... │
│     User question: What is the average salary?"            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 3. LLM PROVIDER LOOKUP (app/models/factory.py)             │
│    Check: LLM_PROVIDER env var                             │
│    ├─ If "openai" → OpenAIClient                           │
│    └─ If "groq" → GroqClient                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 4. API CALL (app/models/openai_client.py or groq_client.py)│
│    Send prompt to LLM cloud service                         │
│    Wait for response                                        │
│    Handle timeouts & errors                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 5. RAW LLM RESPONSE                                         │
│    "Thought: I need to load the CSV and calculate average  │
│     Action: python_code                                    │
│     ```python                                              │
│     import pandas as pd                                    │
│     df = pd.read_csv('data/sample.csv')                    │
│     avg = df['salary'].mean()                             │
│     ```"                                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 6. PARSING (app/agent/parser.py)                           │
│    Extract using regex patterns:                           │
│    • thought: "I need to load the CSV..."                 │
│    • action: "python_code"                                │
│    • code: "import pandas as pd\ndf = ..."               │
│    • final_answer: None                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 7. ACTION EXECUTION                                         │
│    Since action = "python_code":                           │
│    → Call execute_python(code)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 8. CODE EXECUTION (app/tools/python_executor.py)           │
│    Execute code in persistent environment:                 │
│    • df is loaded                                          │
│    • avg = 70000.0 calculated                              │
│    • Return: "{'avg': 70000.0, ...}"                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 9. MEMORY UPDATE (app/memory/buffer.py)                    │
│    Store in memory:                                        │
│    • "Q: What is average salary?"                          │
│    • "Result: avg = 70000.0"                               │
│    (Keep last 5 items)                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 10. LOOP DECISION                                           │
│     Is this a final answer?                                │
│     NO → Continue to step 2 with new context               │
│     Step 2 will build new prompt with memory               │
└──────────────────────┬──────────────────────────────────────┘
                       │
    (Next iteration if needed)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 11. FINAL ITERATION                                         │
│     Thought: "I have the answer"                            │
│     Action: final_answer                                   │
│     Answer: "The average salary is $70,000"               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 12. RETURN TO USER (app/main.py)                            │
│     Display: "✅ Final Answer: The average salary is $70,000"
└─────────────────────────────────────────────────────────────┘
```

---

## Component Interactions

### Detailed Interaction Sequence

```
User
  │
  │ types question
  ▼
┌──────────────────────────┐
│ main.py                  │
│ - Gets user input        │
│ - Calls agent.run()      │
└──────────────┬───────────┘
               │
               ▼
        ┌──────────────────────────┐
        │ SingleAgent.run()        │
        │ (agent.py)              │
        │ for step in range(5):    │
        └──────────┬───────────────┘
                   │
        ┌──────────▼──────────┐
        │ 1. build_prompt()   │     Needs:
        │ (prompt.py)         │  - user_input ← from main
        └──────────┬──────────┘  - memory ← from buffer
                   │             - data_file ← from agent
                   │
        ┌──────────▼────────────────────┐
        │ 2. create_llm_client()         │  Returns:
        │ (factory.py)                   │  - LLMClient instance
        │ ├─ read LLM_PROVIDER env       │
        │ ├─ create OpenAIClient() OR    │
        │ └─ create GroqClient()         │
        └──────────┬────────────────────┘
                   │
        ┌──────────▼────────────────────┐
        │ 3. llm.generate_response()     │  Contacts:
        │ (openai_client.py or          │  - OpenAI API
        │  groq_client.py)              │    OR
        │ │                             │  - Groq API
        │ └─ calls external API ──────────→ [LLM Cloud]
        │                               │    ↓ returns
        └──────────┬────────────────────┘   response
                   │
        ┌──────────▼────────────────────┐
        │ 4. parse_agent_response()      │  Extracts:
        │ (parser.py)                    │  - thought
        │ ├─ regex for "Thought:"        │  - action
        │ ├─ regex for "Action:"         │  - code
        │ ├─ regex for code block        │  - final_answer
        │ └─ regex for "Final Answer:"   │
        └──────────┬────────────────────┘
                   │
        ┌──────────▼────────────────────┐
        │ 5. Decision Branching          │
        │ (agent.py)                     │
        │                                │
        │ if action=="python_code":      │ ─→ execute_python()
        │ elif action=="final_answer":   │ ─→ return answer
        │ else: continue loop            │
        └──────────┬────────────────────┘
                   │
        ┌──────────▼────────────────────────┐
        │ 6a. execute_python()               │
        │ (python_executor.py)               │
        │ ├─ exec(code, _EXECUTION_ENV)     │
        │ └─ returns result                  │
        │                         ↓         │
        │         ┌───────────────────────┐ │
        │         │ _EXECUTION_ENV        │ │
        │         │ (persistent state)    │ │
        │         │ {'df': DataFrame,     │ │
        │         │  'avg': 70000.0, ...} │ │
        │         └───────────────────────┘ │
        └──────────┬────────────────────────┘
                   │
        ┌──────────▼────────────────────┐
        │ 7. memory.add()                │  Store in:
        │ (memory/buffer.py)             │  └─ data: [...]
        │ ├─ append question              │
        │ ├─ append result                │
        │ └─ keep last 5 items            │
        └──────────┬────────────────────┘
                   │
        ┌──────────▼────────────────────┐
        │ 8. Check loop condition        │
        │ if action=="final_answer"      │ ─→ Break loop
        │ else:                          │ ─→ Continue
        │   update user_input with       │    (go to step 1)
        │   "Observation: ..."           │
        └──────────┬────────────────────┘
                   │
            [Loop continues or exits]
                   │
        ┌──────────▼────────────────────┐
        │ 9. Return answer to main.py    │
        └──────────┬────────────────────┘
                   │
        ┌──────────▼────────────────┐
        │ main.py                    │
        │ print("✅ Final Answer: ...")
        └────────────────────────────┘
```

---

## State Management

### Persistent State Components

```
┌─────────────────────────────────────────────────────────┐
│              STATE MANAGEMENT OVERVIEW                   │
└─────────────────────────────────────────────────────────┘

1. EXECUTION STATE (Global in python_executor.py)
   ├─ Scope: Process-wide
   ├─ Lifetime: Until agent finishes or reset
   ├─ Content: Variables from executed code
   │   • df = DataFrame
   │   • result = computation
   │   • temp_var = temp value
   └─ Access: Every code execution

2. MEMORY STATE (Instance in MemoryBuffer)
   ├─ Scope: Current agent instance
   ├─ Lifetime: Until agent.run() completes
   ├─ Content: Last 5 interactions
   │   • Previous questions
   │   • Analysis results
   │   • Observations
   └─ Access: Each loop iteration via memory.get_context()

3. AGENT STATE (Instance in SingleAgent)
   ├─ Scope: Current agent instance
   ├─ Lifetime: Until user exits main loop
   ├─ Content:
   │   • current_data_file path
   │   • llm client
   │   • memory buffer
   └─ Mutable: current_data_file can change

4. CONFIG STATE (Singleton in config.py)
   ├─ Scope: Application-wide
   ├─ Lifetime: Entire application run
   ├─ Content: Settings from .env
   │   • LLM_PROVIDER
   │   • API_KEYs
   │   • MAX_STEPS
   └─ Mutable: Can be changed at module reload
```

### State Reset Points

```
When State is Reset:
├─ On Application Start
│  └─ New SingleAgent instance created
│  └─ Execution environment cleared
│
├─ On File Load
│  └─ pd module still available
│  └─ Previous variables cleared (optional)
│
├─ Between Runs (manual)
│  └─ Call reset_execution_env()
│
└─ On Agent Destruction
   └─ Memory buffer cleared
   └─ LLM client connection closed
```

---

## Extension Points

### How to Add New Features

#### 1. Add New LLM Provider

```python
# Create app/models/anthropic_client.py
from anthropic import Anthropic
from app.models.base import LLMProvider

class AnthropicClient(LLMProvider):
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS
        )
        return response.content[0].text.strip()

# Update app/models/factory.py
elif provider == "anthropic":
    return AnthropicClient()

# Update .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-3-opus
```

#### 2. Add New Tool

```python
# Create app/tools/web_tool.py
import requests

class WebTool:
    @staticmethod
    def fetch_data(url: str) -> dict:
        response = requests.get(url)
        return response.json()

# Make available in executor
_EXECUTION_ENV['WebTool'] = WebTool

# Now LLM can use it:
# data = WebTool.fetch_data('https://api.example.com/data')
```

#### 3. Add Database Support

```python
# Create app/tools/database_tool.py
import sqlalchemy as sql

class DatabaseTool:
    def __init__(self, connection_string: str):
        self.engine = sql.create_engine(connection_string)
    
    def query(self, sql_query: str) -> pd.DataFrame:
        return pd.read_sql(sql_query, self.engine)

# Update main.py
db_tool = DatabaseTool("postgresql://user:pass@host/db")
agent.tools['db'] = db_tool

# LLM can now use:
# df = db.query("SELECT * FROM users")
```

#### 4. Custom Memory Strategy

```python
# Create app/memory/semantic_buffer.py
import numpy as np
from sklearn.embeddings import ...

class SemanticMemoryBuffer:
    """Uses embeddings to retrieve similar past interactions"""
    
    def get_context(self, user_input: str):
        # Embed current input
        # Find k most similar past items
        # Return as context
        pass
```

---

## Error Handling

### Exception Flow

```
User Input
    │
    ▼
┌──────────────────┐
│ Main Try-Except  │ ← Catches: KeyboardInterrupt, Generic Exception
└────────┬─────────┘
         │
    ┌────▼────────────┐
    │ Agent.run()     │ ← Catches: Per-step exceptions
    √────────┬────────┘
             │
    ┌────────▼────────────────┐
    │ LLM API Call            │ ← May raise: Timeout, Auth, RateLimit
    └────────┬────────────────┘
             │
    ┌────────▼────────────────┐
    │ Code Execution          │ ← May raise: NameError, SyntaxError, etc.
    │ (wrapped in exec)       │
    └────────┬────────────────┘
             │
    ┌────────▼────────────────┐
    │ Logging Module          │ ← May raise: File/Permission errors
    └────────┬────────────────┘
             │
         [Logged]
             │
    ┌────────▼────────────────┐
    │ Return Error Message    │ ← User sees friendly error
    └─────────────────────────┘
```

---

## Performance Considerations

### Optimization Opportunities

```
Component          | Bottleneck        | Solution
─────────────────────────────────────────────────────
LLM API Call       | Network latency   | Caching, batching
Code Execution     | Large data        | Streaming, chunking
Memory Buffer      | String concat     | Efficient storage
Prompt Building    | Template building | Pre-compiled templates
Parser             | Regex matching    | Compiled patterns
```

### Caching Strategy (Future)

```python
class CachedLLMClient:
    def __init__(self, base_client):
        self.base_client = base_client
        self.cache = {}
        self.ttl = 3600  # 1 hour
    
    def generate_response(self, prompt: str) -> str:
        hash_val = hash(prompt)
        if hash_val in self.cache:
            return self.cache[hash_val]
        
        response = self.base_client.generate_response(prompt)
        self.cache[hash_val] = response
        return response
```

---

End of Architecture Document
