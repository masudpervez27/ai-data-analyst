from pydantic import BaseModel
from typing import Optional

class AgentResponse(BaseModel):
    thought: str
    action: str
    code: Optional[str] = None
    final_answer: Optional[str] = None