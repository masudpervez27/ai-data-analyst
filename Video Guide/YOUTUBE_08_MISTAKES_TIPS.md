# ⚠️ PART 8: COMMON MISTAKES & OPTIMIZATION TIPS
## Duration: 2-3 minutes | ~900 words

---

## 📍 SCREEN: You at desk, reference materials on screen

---

### [SECTION INTRO]

**YOU:**
"I've helped build a lot of these agents. And I've seen the same mistakes over and over.

Let me save you from making them."

*Serious tone, credible*

**YOU:**
"Here are the real problems people run into, and how to avoid them."

---

## [MISTAKE #1: Prompts That Are Too Vague]

**YOU:**
"Everyone's first prompt is vague."

*Show bad example:*

```
BAD PROMPT:
"Analyze the data and tell me what's important."
```

**YOU:**
"The LLM has no clue what 'important' means in your context. You'll get garbage."

*Show good example:*

```
GOOD PROMPT:
"Analyze the data and identify:
1. Variables with highest correlation to salary
2. Outliers (values > 2 standard deviations from mean)
3. Trends over time if timestamps exist
4. Recommendations for next data collection

Format: Use bullet points. Show calculations."
```

**YOU (voiceover):**
"The good prompt is specific. It tells the LLM exactly what to do, in what format.

Result? You get usable output."

*Back to you*

**YOU:**
"Rule of thumb: If a human would be confused by the prompt, so will the LLM.

Assume the LLM knows nothing about your domain. Over-explain. You'll thank yourself."

---

## [MISTAKE #2: Not Handling Parsing Failures]

**YOU:**
"Part Five showed you the parser. It uses regex to extract code and answers.

But what if the LLM returns something unexpected?"

*Show code:*

```python
# BAD: Assumes parsing always works
parsed = parse_agent_response(raw_response)
code_to_run = parsed.code  # Crash if parse_agent_response returns None!

# GOOD: Validates before using
parsed = parse_agent_response(raw_response)
if parsed is None or parsed.code is None:
    # Try again with corrected prompt
    print("Parsing failed. Retrying with simpler prompt...")
    return agent.run(user_input)

code_to_run = parsed.code
```

**YOU:**
"Always validate. Assume the system will fail sometimes. Build in recovery."

---

## [MISTAKE #3: Code Execution Without Timeouts]

**YOU:**
"The agent can generate infinite loops."

*Show dangerous code:*

```python
# DANGEROUS: No timeout
result = execute_python(agent_generated_code)
# If code has: while True: ... the agent freezes forever!
```

**YOU:**
"Always add timeouts to execution:"

*Show safe code:*

```python
# SAFE: Timeout prevents hanging
try:
    result = execute_python(agent_generated_code, timeout=5)  # 5 seconds max
except TimeoutError:
    print("Code took too long. Probably an infinite loop.")
    print("Asking agent to refactor...")
```

**YOU:**
"5 seconds. Adjust based on your needs. But never run agent code without limits."

---

## [MISTAKE #4: Token Limits On Long Conversations]

**YOU:**
"Your agent builds up context as it goes. More context = more tokens = higher costs."

*Show the problem:*

```
Interaction 1: 150 tokens used
Interaction 2: 300 tokens (includes Interaction 1 context)
Interaction 3: 600 tokens (includes both previous)
Interaction 4: 1,200 tokens
...
By Interaction 10: 76,800 tokens! Your costs explode.
```

**YOU:**
"Solution: Cap your context window."

*Show solution:*

```python
# Keep only last 5 interactions in memory
MAX_MEMORY_SIZE = 5

class MemoryBuffer:
    def add(self, item):
        self.items.append(item)
        if len(self.items) > MAX_MEMORY_SIZE:
            self.items.pop(0)  # Remove oldest
```

**YOU:**
"Rolling window. Always keep your memory bounded."

---

## [MISTAKE #5: Not Logging What The Agent Does]

**YOU:**
"When something goes wrong, you need to know why."

*Show what NOT to do:*

```python
# BAD: Silent failure
def run_agent(question):
    try:
        return agent.run(question)
    except:
        return "Error"  # Tell me NOTHING
```

**YOU:**
"You have no idea what failed. Was it the API? The code? The parser?"

*Show what TO do:*

```python
# GOOD: Detailed logging
logger.info(f"User asked: {question}")
logger.debug(f"Building prompt...")
raw_response = llm.generate_response(prompt)
logger.debug(f"LLM returned: {raw_response[:100]}...")  # First 100 chars
parsed = parse_agent_response(raw_response)
logger.debug(f"Parsed action: {parsed.action}")

if parsed.action == "python_code":
    logger.info(f"Executing code...")
    result = execute_python(parsed.code)
    logger.debug(f"Code result: {result}")
```

**YOU:**
"Every major step gets logged. When something breaks, you can see exactly where.

Use a structured logger like Python's logging module. Not print() statements.

Print statements get lost in production. Logs are queryable."

---

## [OPTIMIZATION TIP #1: Batch Similar Queries]

**YOU:**
"If you have multiple questions, don't run the agent once per question."

*Show inefficient approach:*

```python
# Slow: Creates 100 agent instances, makes 100 API calls
for question in 100_questions:
    answer = agent.run(question)
```

**YOU:**
"Group them together:"

*Show optimized approach:*

```python
# Fast: One agent, combined prompt
combined_prompt = "Answer these 100 questions: " + "\n".join(100_questions)
all_answers = agent.run(combined_prompt)
```

**YOU:**
"One API call. Faster. Cheaper. The LLM is actually better at comparing across questions."

---

## [OPTIMIZATION TIP #2: Cache LLM Responses]

**YOU:**
"Users ask similar questions. Don't re-ask the LLM."

*Show caching:*

```python
class CachedAgent:
    def __init__(self):
        self.cache = {}
        self.agent = SingleAgent()
    
    def run(self, question):
        if question in self.cache:
            logger.info("Returning cached answer")
            return self.cache[question]
        
        answer = self.agent.run(question)
        self.cache[question] = answer
        return answer
```

**YOU:**
"Same question asked twice? Second time is instant."

---

## [OPTIMIZATION TIP #3: Use Cheaper Models For Simple Tasks]

**YOU:**
"Not every task needs GPT-4."

*Show provider optimization:*

```python
def choose_model(question):
    if len(question) < 50 and question.count(' ') < 10:
        # Simple question: Use cheap fast model
        return "groq"
    else:
        # Complex question: Use powerful model
        return "openai"

LLM_PROVIDER = choose_model(user_question)
agent = SingleAgent()
answer = agent.run(user_question)
```

**YOU:**
"Groq for quick lookups. OpenAI for complex analysis. Different tools for different jobs.

You'll cut costs by 70%."

---

## [DEBUGGING TECHNIQUE: Temperature Adjustment]

**YOU:**
"The LLM has a parameter called 'temperature.'

Low temperature = same answer every time (reliable)  
High temperature = creative, varied (but unpredictable)"

*Show in config:*

```python
# In config.py
GROQ_TEMPERATURE = 0.3  # Low: Consistent, predictable behavior

# For brainstorming prompts:
GROQ_TEMPERATURE = 0.9  # High: Creative, diverse outputs
```

**YOU:**
"For data analysis, use low temperature. For creative tasks, use high.

Adjust based on what you need."

---

## [FINAL DEBUGGING RULE]

**YOU:**
"If the agent gives you a bad answer, don't blame the LLM.

99% of the time, it's one of five things:"

*Count on fingers:*

```
1. Vague prompt
2. Incomplete context
3. The data is garbage
4. Parser is failing silently
5. Timeout cut off execution
```

**YOU:**
"Debug in this order. Nine times out of ten, you'll find the problem."

---

## [TRANSITION]

**YOU:**
"We've built it. We've shown it working. We've scaled it. We've debugged it.

Now it's time to bring everything home."

---

## 📝 TECHNICAL NOTES FOR FILMING:

- **Energy:** This section is practical and advice-focused. Keep it grounded but helpful.
- **Pacing:** Each mistake/tip should be quick (15-30 seconds each)
- **Visuals:** Show code side-by-side (bad vs. good)

---

## ✅ CHECKPOINT

**Status:** Part 8 Complete - Mistakes & Tips  
**Next:** Part 9 - Closeout & Call to Action  
**Total Duration So Far:** 39-48 minutes  
**Duration Remaining:** ~2-3 minutes (FINAL SECTION)

---

**Continue with Part 9 (Closeout & CTA)?**
