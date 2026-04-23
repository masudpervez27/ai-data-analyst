"""
Legacy LLMClient - Use factory.create_llm_client() for new code.

This module is kept for backward compatibility.
Prefer app.models.factory.create_llm_client() in new code.
"""

from app.models.factory import create_llm_client

# Backward compatibility alias
LLMClient = type(
    'LLMClient',
    (),
    {
        '__doc__': 'Deprecated: Use create_llm_client() from app.models.factory instead',
        '__init__': lambda self: self.__dict__.update(create_llm_client().__dict__),
        '__getattr__': lambda self, name: getattr(create_llm_client(), name),
    }
)

__all__ = ['LLMClient']
