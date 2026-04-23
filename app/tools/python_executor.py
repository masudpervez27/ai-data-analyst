import traceback
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Persistent execution environment to maintain state across calls
_EXECUTION_ENV = {
    "__builtins__": __builtins__,
}


def execute_python(code: str) -> str:
    """Execute Python code with persistent state across calls.
    
    This maintains variable state between executions so that variables
    created in one step are available in subsequent steps.
    
    Args:
        code: Python code to execute
        
    Returns:
        String representation of the execution result or error traceback
    """
    try:
        # Import commonly needed libraries if not already present
        if 'pd' not in _EXECUTION_ENV:
            import pandas as pd
            _EXECUTION_ENV['pd'] = pd
        
        # Execute code in persistent environment
        exec(code, _EXECUTION_ENV)
        
        # Return only new variables created (excluding builtins and imports)
        result_vars = {k: v for k, v in _EXECUTION_ENV.items() 
                      if not k.startswith('__') and k not in ['pd']}
        
        logger.debug(f"Execution completed. Available vars: {list(result_vars.keys())}")
        return str(result_vars) if result_vars else "Code executed successfully"
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.error(f"Execution error: {error_msg}")
        return error_msg


def reset_execution_env():
    """Reset the persistent execution environment."""
    global _EXECUTION_ENV
    _EXECUTION_ENV = {"__builtins__": __builtins__}
    logger.info("Execution environment reset")
    