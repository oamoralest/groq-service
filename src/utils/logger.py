"""
Logging configuration for the Groq service.
Provides structured logging with environment-specific settings.
"""
import logging
import sys
from typing import Any, Dict

from ..config import get_config

def setup_logger(name: str = "groq_service") -> logging.Logger:
    """
    Set up a logger with the specified configuration.
    
    Args:
        name: The name of the logger
        
    Returns:
        A configured logger instance
    """
    config = get_config()
    logger = logging.getLogger(name)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set log level based on environment
    log_level = getattr(logging, config.LOG_LEVEL.upper())
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

def log_request(logger: logging.Logger, method: str, url: str, **kwargs: Any) -> None:
    """Log API request details."""
    logger.debug(f"Request: {method} {url}", extra={
        "method": method,
        "url": url,
        **kwargs
    })

def log_response(logger: logging.Logger, status_code: int, response_time: float, **kwargs: Any) -> None:
    """Log API response details."""
    logger.debug(f"Response: {status_code} ({response_time:.2f}s)", extra={
        "status_code": status_code,
        "response_time": response_time,
        **kwargs
    })

def log_error(logger: logging.Logger, error: Exception, context: Dict[str, Any]) -> None:
    """Log error details with context."""
    logger.error(
        f"Error: {str(error)}",
        extra={"error_type": type(error).__name__, **context},
        exc_info=True
    )

# Create default logger instance
logger = setup_logger() 