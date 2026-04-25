# 🎬 PART 5: BUILDING IT LIVE
## Duration: 12-14 minutes | ~2400 words

---

## 📍 SCREEN: You at computer, screen recording + face camera split

---

### [SECTION INTRO]

*You on camera, looking excited*

**YOU:**
"Alright, time to build. If you've been paying attention, you understand what an agent is and how it works. Now let's actually write the code."

*Shift to show screen*

**YOU (voiceover):**
"I'm going to show you every key file we need, explain what each one does, and show you the actual code. Don't worry if you can't read everything—I'll break it down."

---

### [SETUP & PREREQUISITES]

*Screen shows: Terminal with installation commands*

**YOU:**
"First, prerequisites. You need:

Python 3.13 or higher
An API key from either OpenAI or Groq (or both)
About 10 minutes to set this up"

*Show on screen:*

**YOU (voiceover):**
"Installation is simple. Clone the repo or create a new folder. Then run: `uv sync` or `pip install -e .` if you're using pip."

*Show .env file on screen*

**YOU:**
"Then create a .env file in your project root and add your API keys. Here's what it looks like:"

*Show example .env:*

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk-your-key-here
MAX_STEPS=5
```

**YOU (voiceover):**
"One line tells the system which provider to use. Groq is cheaper and faster, so I recommend starting there. But you can switch to OpenAI anytime."

---

### [FOLDER STRUCTURE]

*Show file tree on screen, growing as you explain*

**YOU:**
"Let me show you the folder structure. It looks like this:"

*Screenshot showing:*

```
ai-data-analyst/
├── app/
│   ├── main.py              ← Entry point
│   ├── agent/
│   │   ├── agent.py         ← The brain
│   │   ├── prompt.py        ← Instructions
│   │   └── parser.py        ← Extract response
│   ├── models/
│   │   ├── base.py          ← Interface
│   │   ├── openai_client.py ← OpenAI
│   │   ├── groq_client.py   ← Groq
│   │   └── factory.py       ← Switcher
│   ├── tools/
│   │   └── python_executor.py ← Run code
│   ├── memory/
│   │   └── buffer.py        ← Remember stuff
│   └── core/
│       ├── config.py        ← Settings
│       └── logger.py        ← Logging
├── data/
│   └── sample.csv           ← Your data
└── .env                     ← API keys
```

**YOU (voiceover):**
"Notice how it's organized? Every component has its own place. This makes it easy to find things and modify them."

---

### [FILE EXPLANATIONS & CODE SNIPPETS]

*Screen switches between files and you explaining*

---

#### FILE 1: main.py (Entry Point)

*Show code on screen*

**YOU:**
"File One: `main.py`. This is where the user interacts with the agent.

Here's the code:"

*Display on screen:*

```python
from app.agent.agent import SingleAgent

def main():
    agent = SingleAgent()
    
    while True:
        query = input("\nAsk: ")
        if query.lower() == "exit":
            break
        
        answer = agent.run(query)
        print("\n✅ Final Answer:", answer)

if __name__ == "__main__":
    main()
```

**YOU:**
"What's happening here? It's simple:

One - Create an agent

Two - Start a loop

Three - Ask the user for a question

Four - Run the agent

Five - Show the answer

That's literally it. The complexity is hidden inside the agent object."

---

#### FILE 2: agent.py (The Brain)

*Show agent.py on screen*

**YOU:**
"File Two: `agent.py`. This is the brain. Where all the decision-making happens.

Here's the main function:"

*Display on screen:*

```python
class SingleAgent:
    def __init__(self):
        self.llm = create_llm_client()
        self.memory = MemoryBuffer()
    
    def run(self, user_input: str):
        for step in range(settings.MAX_STEPS):
            prompt = build_prompt(user_input, self.memory.get_context())
            raw_output = self.llm.generate_response(prompt)
            parsed = parse_agent_response(raw_output)
            
            if parsed.action == "final_answer":
                return parsed.final_answer
            elif parsed.action == "python_code":
                result = execute_python(parsed.code)
                self.memory.add(result)
                user_input = f"Observation: {result}"
```

**YOU:**
"Look at this loop. This is the agent loop in code.

Step one: Build a prompt

Step two: Send to LLM anduate get response

Step three: Parse the response

Step four: If it's a final answer, return it

Step five: If it's code, execute it

Step six: Loop back"

*Point to each section*

**YOU (voiceover):**
"This eight-line loop? This is literally the core of the agent. Everything else is supporting this."

---

#### FILE 3: prompt.py (Instructions)

*Show prompt.py on screen*

**YOU:**
"File Three: `prompt.py`. This is where we tell the LLM what to do.

Here's what it looks like:"

*Display on screen:*

```python
def build_prompt(user_input: str, memory: str) -> str:
    return f"""You are a professional AI data analyst.

AVAILABLE RESOURCES:
- pandas library (imported as 'pd')
- Data file: 'data/sample.csv'

INSTRUCTIONS:
Output EXACTLY in this format:

Thought: [Your reasoning]
Action: python_code OR final_answer

If python_code:
```python
df = pd.read_csv('data/sample.csv')
result = df['salary'].mean()
```

If final_answer:
Final Answer: [Your answer]

Memory:
{memory}

User request:
{user_input}

Now respond:"""
```

**YOU:**
"See what we're doing? We're being super explicit about:

One - What tools the LLM has available

Two - Exactly how we want the response formatted

Three - Previous context (memory)

Four - The actual question"

*Lean forward*

**YOU (voiceover):**
"This prompt engineering determines if the agent works well or not. Good prompt → good results. Bad prompt → garbage."

---

#### FILE 4: parser.py (Extract Response)

*Show parser.py on screen*

**YOU:**
"File Four: `parser.py`. The LLM outputs messy text. This file extracts the structured parts.

Here's what it does:"

*Display on screen:*

```python
import re

def parse_agent_response(response: str) -> AgentResponse:
    thought_pattern = r"Thought:\s*([^\n]*)"
    action_pattern = r"Action:\s*([^\n]*)"
    code_pattern = r"```(?:python)?\s*(.+?)```"
    final_answer_pattern = r"Final Answer:\s*(.+?)(?:\n|$)"
    
    thought = re.search(thought_pattern, response).group(1) if ... else ""
    action = re.search(action_pattern, response).group(1) if ... else ""
    code = re.search(code_pattern, response, re.DOTALL).group(1) if ... else None
    final_answer = re.search(final_answer_pattern, response).group(1) if ... else None
    
    return AgentResponse(
        thought=thought,
        action=action,
        code=code,
        final_answer=final_answer
    )
```

**YOU:**
"This uses regular expressions—regex—to find patterns in the text.

Looking for 'Thought:' and pulling what comes after.

Looking for code blocks and extracting the code.

It's turning messy text into structured data."

*Show example on screen: Raw messy response → Structured JSON*

**YOU (voiceover):**
"This is crucial because the next component needs clean data to work with."

---

#### FILE 5: python_executor.py (Run Code Safely)

*Show python_executor.py on screen*

**YOU:**
"File Five: `python_executor.py`. This runs Python code safely.

Here's the clever part:"

*Display on screen:*

```python
_EXECUTION_ENV = {
    "__builtins__": __builtins__,
}

def execute_python(code: str) -> str:
    # Pre-import pandas
    if 'pd' not in _EXECUTION_ENV:
        import pandas as pd
        _EXECUTION_ENV['pd'] = pd
    
    # Execute code in persistent environment
    exec(code, _EXECUTION_ENV)
    
    # Return the results
    return str(_EXECUTION_ENV)
```

**YOU:**
"The key insight here: `_EXECUTION_ENV` is a global dictionary that persists across calls.

So if Step One creates a variable 'df', Step Two can use that same 'df'.

Without this, every code execution would start from scratch and the agent couldn't build on previous work."

*Gestures expressively*

**YOU (voiceover):**
"This persistent state is what makes multi-step reasoning possible."

---

#### FILE 6: LLM Providers (The Flexibility)

*Show both files side by side*

**YOU:**
"Files Six & Seven: The LLM providers.

This is where the flexibility comes in. We have two separate implementations:"

*Show openai_client.py on screen:*

```python
from openai import OpenAI

class OpenAIClient(LLMProvider):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS
        )
        return response.choices[0].message.content.strip()
```

**YOU:**
"OpenAI implementation. Connects to OpenAI's API."

*Show groq_client.py on screen:*

```python
from groq import Groq

class GroqClient(LLMProvider):
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    def generate_response(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS
        )
        return chat_completion.choices[0].message.content.strip()
```

**YOU:**
"Groq implementation. Similar structure, different API.

Now look at the factory:"

*Show factory.py:*

```python
def create_llm_client() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "openai":
        return OpenAIClient()
    elif provider == "groq":
        return GroqClient()
```

**YOU (voiceover):**
"One function decides which client to use based on settings.

Want to switch from Groq to OpenAI? Change one line in .env.

That's it. Everything else stays the same. This is the power of good design."

---

#### FILE 7: config.py (Settings)

*Show config.py on screen*

**YOU:**
"File Eight: `config.py`. All your settings live here.

Quick look:"

*Display:*

```python
class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = "mixtral-8x7b-32768"
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-4o-mini"
    
    MAX_STEPS = 5
    MAX_TOKENS = 150
```

**YOU:**
"All the 'knobs and dials' in one place. Change something here, the whole app adapts."

---

#### FILE 8: memory/buffer.py (Short-term Memory)

*Show buffer.py on screen*

**YOU:**
"File Nine: `memory/buffer.py`. The agent's short-term memory.

Simple but powerful:"

*Display:*

```python
class MemoryBuffer:
    def __init__(self, k=5):
        self.k = k
        self.data = []
    
    def add(self, item: str):
        self.data.append(item)
    
    def get_context(self):
        return "\n".join(self.data[-self.k:])
```

**YOU:**
"The agent stores items in memory. When it needs context, it pulls the last 5 items.

This is why the agent can reference what happened before instead of starting from scratch every time."

---

### [SWITCHING PROVIDERS - LIVE DEMO]

*Show on screen: .env file*

**YOU:**
"Now let me show you the magic: Switching providers.

Currently it's set to Groq."

*Show:*

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk-your-key
```

**YOU (voiceover):**
"To switch to OpenAI, I just change this:"

*Editing the file as you speak*

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
```

**YOU:**
"That's it. Nothing else changes. No code modifications. The factory pattern does the work."

*Point to camera*

**YOU:**
"This is what good software architecture looks like."

---

### [CONFIGURATION WALKTHROUGH]

**YOU:**
"There are also a few configuration options to understand:

`MAX_STEPS`: How many times the agent loops before giving up. Default is 5.

`MAX_TOKENS`: Maximum length of the LLM's response. 150 is good for most queries.

If you want longer analyses, increase this. If you want faster responses, decrease it."

*Show settings on screen*

**YOU (voiceover):**
"These are the levers you pull to tune the agent's behavior."

---

### [TRANSITION TO DEMO]

**YOU:**
"Alright, so that's the architecture in code. Every file has a purpose. Everything connects.

Now let's see it in action."

---

## 📝 TECHNICAL NOTES FOR FILMING:

- **Screen Recording:** Use zoomed-in font so code is readable
- **Pacing:** Slow enough for viewers to read code
- **Highlights:** Maybe use syntax highlighting or color overlays
- **Transitions:** Smooth between files, don't jump abruptly

---

## ✅ CHECKPOINT

**Status:** Part 5 Complete - Building Live  
**Next:** Part 6 - Demo & Results  
**Total Duration So Far:** 28-34 minutes  
**Duration Remaining:** ~6-17 minutes

---

**Continue with Part 6 (Demo)?**
