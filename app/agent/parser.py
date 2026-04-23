import re
from app.schemas.agent_schema import AgentResponse
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def parse_agent_response(response: str) -> AgentResponse:
    """Parse the agent response with improved regex patterns and fallback logic.
    
    Args:
        response: The raw LLM response text
        
    Returns:
        AgentResponse with parsed thought, action, code, and final_answer
    """
    logger.debug(f"Raw LLM Response:\n{response}\n---")
    
    # Updated patterns - more flexible extraction
    thought_pattern = r"Thought:\s*([^\n]*)"
    action_pattern = r"Action:\s*([^\n]*)"
    # More flexible code block pattern - handles various formatting
    code_pattern = r"```(?:python)?\s*(.+?)```"
    final_answer_pattern = r"Final Answer:\s*(.+?)(?:\n|$)"

    thought_match = re.search(thought_pattern, response, re.IGNORECASE)
    action_match = re.search(action_pattern, response, re.IGNORECASE)
    code_match = re.search(code_pattern, response, re.DOTALL)
    final_answer_match = re.search(final_answer_pattern, response, re.DOTALL | re.IGNORECASE)

    thought = thought_match.group(1).strip() if thought_match else ""
    action = action_match.group(1).strip().lower() if action_match else ""
    code = code_match.group(1).strip() if code_match else None
    final_answer = final_answer_match.group(1).strip() if final_answer_match else None

    # Normalize action string - handle variations
    if "python" in action or "code" in action:
        action = "python_code"
    elif "final" in action or "answer" in action:
        action = "final_answer"
    
    # Log extraction results
    logger.debug(f"Parsed - Thought: '{thought}' | Action: '{action}' | Has Code: {code is not None} | Answer: '{final_answer}'")

    return AgentResponse(
        thought=thought,
        action=action,
        code=code,
        final_answer=final_answer
    )