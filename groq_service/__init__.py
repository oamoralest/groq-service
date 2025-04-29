"""
Groq Service - A Python service for interacting with Groq's API.
"""

from .client import GroqClient
from .api import app as api_app
from .server import main as run_server
from .cli import main as cli_main

__version__ = "0.1.0"
__all__ = ["GroqClient", "api_app", "run_server", "cli_main"] 