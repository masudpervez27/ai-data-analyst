from app.core.config import settings
from app.models.base import LLMProvider
from app.models.openai_client import OpenAIClient
from app.models.groq_client import GroqClient
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def create_llm_client() -> LLMProvider:
    """Factory function to create the appropriate LLM client based on config.
    
    Returns:
        An instance of the configured LLM provider (OpenAIClient or GroqClient)
        
    Raises:
        ValueError: If the configured provider is not supported
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "openai":
        logger.info("Initializing OpenAI client")
        return OpenAIClient()
    elif provider == "groq":
        logger.info("Initializing Groq client")
        return GroqClient()
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: openai, groq"
        )
