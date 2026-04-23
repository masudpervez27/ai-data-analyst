def build_prompt(user_input: str, memory: str) -> str:
    """Build a structured prompt that guides the LLM toward consistent formatting.
    
    Args:
        user_input: The user's question or observation
        memory: The context from memory buffer
        
    Returns:
        A structured prompt string
    """
    return f"""You are a professional AI data analyst agent specializing in data analysis with Python.

AVAILABLE RESOURCES:
- pandas library (imported as 'pd')
- Sample data file: 'data/sample.csv' - contains employee data (name, age, salary)
- You can load data with: df = pd.read_csv('data/sample.csv')

INSTRUCTIONS:
1. Analyze the user's request using Python
2. Output EXACTLY in this format:

Thought: [Your reasoning about what to do next]
Action: python_code OR final_answer

If you choose python_code:
```python
# Your Python code here - pandas is already imported as pd
# Load data: df = pd.read_csv('data/sample.csv')
df = pd.read_csv('data/sample.csv')
result = df['salary'].mean()  # Example: calculate average salary
```

If you choose final_answer:
Final Answer: [Your direct answer to the user's question based on previous analysis]

RULES:
- Always pick ONE action per response
- For analysis tasks, choose 'python_code' with executable code
- Variables created in previous steps are available for reuse
- For final results, choose 'final_answer'
- Action names are python_code or final_answer

Memory context (previous steps):
{memory}

User request:
{user_input}

Now respond with Thought, Action, and either code or final answer:"""
