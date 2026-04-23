import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM Provider: "openai" or "groq"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Groq settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Common settings
    MAX_STEPS: int = 5
    MAX_TOKENS: int = 150
    
    @property
    def MODEL_NAME(self) -> str:
        """Get the appropriate model name based on provider."""
        if self.LLM_PROVIDER == "groq":
            return self.GROQ_MODEL
        return self.OPENAI_MODEL
    
    @property
    def API_KEY(self) -> str:
        """Get the appropriate API key based on provider."""
        if self.LLM_PROVIDER == "groq":
            return self.GROQ_API_KEY
        return self.OPENAI_API_KEY

settings = Settings()