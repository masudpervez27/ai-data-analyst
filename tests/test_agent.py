import pytest
from app.agent.agent import SingleAgent

class MockLLM:
    def generate(self, prompt: str) -> str:
        return """
Thought: I can answer directly
Action: final_answer
Final Answer: Test successful
"""

def test_agent_final_answer(monkeypatch):
    agent = SingleAgent()
    agent.llm = MockLLM()

    result = agent.run("Test question")

    assert "Test successful" in result