"""
Groq model implementation using the official groq package.
Supports all available Groq models with a unified interface.
"""
from typing import AsyncGenerator, Dict, Optional, Any, List
import asyncio
from groq import Groq
from groq.types.chat import ChatCompletion

from .base import BaseModel, ModelParameters, ModelResponse
from ..config import get_config
from ..utils.logger import logger
from ..utils.rate_limiter import get_rate_limiter

class GroqModel(BaseModel):
    """Implementation of Groq models using the official client."""
    
    AVAILABLE_MODELS = {
        "llama2-70b-4096": "Llama 2 70B",
        "llama-3.3-70b-versatile": "Llama 3 70B Versatile"
    }
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize the Groq model.
        
        Args:
            model_name: Name of the model to use (default: llama-3.3-70b-versatile)
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not available. Choose from: {list(self.AVAILABLE_MODELS.keys())}")
            
        super().__init__(model_name)
        self.config = get_config()
        self.rate_limiter = get_rate_limiter()
        self.client = Groq(api_key=self.config.GROQ_API_KEY.get_secret_value())

    def _create_messages(self, prompt: str) -> List[Dict[str, str]]:
        """Convert prompt to messages format."""
        return [{"role": "user", "content": prompt}]

    async def complete(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> ModelResponse:
        """Generate a completion for the given prompt."""
        parameters = self._validate_parameters(parameters)
        messages = self._create_messages(prompt)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("completion")
        
        try:
            response: ChatCompletion = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=messages,
                model=self.model_name,
                temperature=parameters.temperature,
                max_tokens=parameters.max_tokens,
                top_p=parameters.top_p,
                stream=False
            )
            
            return ModelResponse(
                text=response.choices[0].message.content,
                finish_reason=response.choices[0].finish_reason,
                model=self.model_name,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"Error during completion: {str(e)}")
            raise

    async def stream(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> AsyncGenerator[str, None]:
        """Stream completions for the given prompt."""
        parameters = self._validate_parameters(parameters)
        messages = self._create_messages(prompt)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("stream")
        
        try:
            # Create streaming response
            stream = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=messages,
                model=self.model_name,
                temperature=parameters.temperature,
                max_tokens=parameters.max_tokens,
                top_p=parameters.top_p,
                stream=True
            )
            
            async for chunk in self._async_iterate(stream):
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            raise

    async def _async_iterate(self, stream):
        """Convert sync iterator to async iterator."""
        for item in stream:
            yield item
            await asyncio.sleep(0)  # Allow other tasks to run

    async def close(self) -> None:
        """Clean up resources."""
        # No cleanup needed for official client
        pass 