from openai import OpenAI
from app.core.config import settings
from app.models.base import LLMProvider


class OpenAIClient(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response(self, prompt: str) -> str:
        """Generate a response using OpenAI API.
        
        Args:
            prompt: The input prompt
            
        Returns:
            The response from OpenAI
        """
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS
        )
        return response.choices[0].message.content.strip()
