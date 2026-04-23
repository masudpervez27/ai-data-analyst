from groq import Groq
from app.core.config import settings
from app.models.base import LLMProvider


class GroqClient(LLMProvider):
    """Groq LLM provider implementation."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate_response(self, prompt: str) -> str:
        """Generate a response using Groq API.
        
        Args:
            prompt: The input prompt
            
        Returns:
            The response from Groq
        """
        chat_completion = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS
        )
        return chat_completion.choices[0].message.content.strip()
