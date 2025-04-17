"""
Type definitions for the Groq service.
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ModelParameters:
    """Parameters for model generation."""
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0


@dataclass
class ModelResponse:
    """Response from model generation."""
    text: str
    finish_reason: str
    model: str
    usage: Dict[str, int] 