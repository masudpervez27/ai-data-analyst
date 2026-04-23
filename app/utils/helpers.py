import re
from typing import Optional

def extract_python_code(text: str) -> Optional[str]:
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def clean_text(text: str) -> str:
    return text.strip().replace("\n\n", "\n")


def truncate(text: str, max_length: int = 500) -> str:
    return text[:max_length] + "..." if len(text) > max_length else text