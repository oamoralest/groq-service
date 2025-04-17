"""
Main client interface for the Groq service.
Provides a high-level interface for interacting with Groq models.
"""
from typing import AsyncGenerator, Optional, Dict, Any, List

from .models.base import ModelParameters, ModelResponse
from .models.groq_model import GroqModel
from .config import get_config
from .utils.logger import logger

class GroqClient:
    """
    High-level client for interacting with Groq models.
    Provides a simple interface for text generation and streaming.
    """
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize the Groq client.
        
        Args:
            model_name: Name of the model to use (default: llama-3.3-70b-versatile)
        """
        self.config = get_config()
        self.model = self._get_model(model_name)
        logger.info(f"Initialized GroqClient with model: {model_name}")

    def _get_model(self, model_name: str) -> GroqModel:
        """Get the appropriate model implementation."""
        return GroqModel(model_name)

    @property
    def available_models(self) -> List[str]:
        """Get list of available models."""
        return list(GroqModel.AVAILABLE_MODELS.keys())

    async def complete(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs: Any
    ) -> str:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model parameters
            
        Returns:
            Generated text
        """
        parameters = ModelParameters(
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        try:
            response = await self.model.complete(prompt, parameters)
            return response.text
        except Exception as e:
            logger.error(f"Error in completion: {str(e)}")
            raise

    async def stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """
        Stream completions for the given prompt.
        
        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model parameters
            
        Yields:
            Generated text chunks
        """
        parameters = ModelParameters(
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        try:
            async for chunk in self.model.stream(prompt, parameters):
                yield chunk
        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            raise

    async def close(self) -> None:
        """Close the client and release resources."""
        await self.model.close()
        logger.info("GroqClient closed") 