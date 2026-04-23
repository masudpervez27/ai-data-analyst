from app.models.factory import create_llm_client
from app.agent.prompt import build_prompt
from app.agent.parser import parse_agent_response
from app.tools.python_executor import execute_python, reset_execution_env
from app.memory.buffer import MemoryBuffer
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class SingleAgent:
    def __init__(self):
        self.llm = create_llm_client()
        self.memory = MemoryBuffer()
        # Reset execution environment for fresh start
        reset_execution_env()

    def run(self, user_input: str):
        """Run the agent loop to answer a user query.
        
        Args:
            user_input: The user's question
            
        Returns:
            The final answer or error message
        """
        for step in range(settings.MAX_STEPS):
            try:
                prompt = build_prompt(user_input, self.memory.get_context())
                raw_output = self.llm.generate_response(prompt)
                
                logger.debug(f"Step {step + 1} - LLM output:\n{raw_output[:300]}...")

                parsed = parse_agent_response(raw_output)

                logger.info(f"\n🧠 Thought: {parsed.thought}")
                logger.info(f"⚙️ Action: {parsed.action}")

                # Check if response is empty (parsing failed)
                if not parsed.action or (not parsed.thought and not parsed.code and not parsed.final_answer):
                    logger.warning(f"Step {step + 1}: Empty response from LLM - retrying")
                    continue

                if parsed.action == "final_answer":
                    if parsed.final_answer:
                        logger.info(f"✅ Final Answer: {parsed.final_answer}")
                        return parsed.final_answer
                    else:
                        logger.warning("Action was 'final_answer' but no answer content found")
                        continue

                elif parsed.action == "python_code":
                    if parsed.code:
                        logger.debug(f"Executing code:\n{parsed.code}")
                        result = execute_python(parsed.code)
                        logger.info(f"📊 Observation: {result[:500]}...")

                        # Store meaningful context in memory
                        self.memory.add(f"Q: {user_input}")
                        self.memory.add(f"Analysis result: {result[:200]}")

                        user_input = f"Previous analysis result:\n{result}\n\nContinue with the analysis or provide a final answer."
                    else:
                        logger.warning(f"Step {step + 1}: Action was 'python_code' but no code block found")
                        logger.debug(f"Full response was:\n{raw_output}")
                        continue
                else:
                    logger.warning(f"Unknown action: {parsed.action}")
                    continue
                    
            except Exception as e:
                logger.error(f"Step {step + 1} error: {str(e)}", exc_info=True)
                continue
        
        return "⚠️ Max analysis steps reached without a final answer"