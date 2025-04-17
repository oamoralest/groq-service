"""
Base model interface for Groq models.
Defines the common interface and functionality that all models must implement.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Optional, Any
from pydantic import BaseModel, Field

class ModelParameters(BaseModel):
    """Common parameters for model inference."""
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(1024, gt=0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    top_k: int = Field(40, ge=0)
    stop: Optional[list[str]] = None
    stream: bool = False

class ModelResponse(BaseModel):
    """Standard response format for model inference."""
    text: str
    finish_reason: Optional[str] = None
    model: str
    usage: Dict[str, int]

class BaseModel(ABC):
    """Abstract base class for all Groq models."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> ModelResponse:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: The input prompt
            parameters: Optional model parameters
            
        Returns:
            A ModelResponse containing the generated text and metadata
        """
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream completions for the given prompt.
        
        Args:
            prompt: The input prompt
            parameters: Optional model parameters
            
        Yields:
            Generated text chunks
        """
        pass

    def _validate_parameters(self, parameters: Optional[ModelParameters]) -> ModelParameters:
        """Validate and return model parameters."""
        return parameters or ModelParameters()

    def _prepare_request(
        self,
        prompt: str,
        parameters: ModelParameters
    ) -> Dict[str, Any]:
        """Prepare the request payload for the API."""
        return {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": parameters.temperature,
            "max_tokens": parameters.max_tokens,
            "top_p": parameters.top_p,
            "top_k": parameters.top_k,
            "stop": parameters.stop,
            "stream": parameters.stream
        } 