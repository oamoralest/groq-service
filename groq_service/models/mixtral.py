"""
Mixtral model implementation for the Groq service.
"""
import json
from typing import AsyncGenerator, Dict, Optional, Any

import httpx

from .base import BaseModel, ModelParameters, ModelResponse
from ..config import get_config
from ..utils.logger import logger
from ..utils.rate_limiter import get_rate_limiter

class MixtralModel(BaseModel):
    """Implementation of the Mixtral-8x7B model."""
    
    def __init__(self):
        super().__init__("mixtral-8x7b-v0.1")
        self.config = get_config()
        self.rate_limiter = get_rate_limiter()
        self.client = httpx.AsyncClient(
            base_url=self.config.GROQ_API_BASE_URL,
            headers={
                "Authorization": f"Bearer {self.config.GROQ_API_KEY.get_secret_value()}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )

    async def complete(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> ModelResponse:
        """Generate a completion for the given prompt."""
        parameters = self._validate_parameters(parameters)
        payload = self._prepare_request(prompt, parameters)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("completion")
        
        try:
            response = await self.client.post("/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            return ModelResponse(
                text=data["choices"][0]["text"],
                finish_reason=data["choices"][0].get("finish_reason"),
                model=self.model_name,
                usage=data["usage"]
            )
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during completion: {str(e)}")
            raise
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
        parameters.stream = True
        payload = self._prepare_request(prompt, parameters)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("stream")
        
        try:
            async with self.client.stream("POST", "/completions", json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            data = json.loads(line.removeprefix("data: "))
                            if data.get("choices"):
                                yield data["choices"][0]["text"]
                        except json.JSONDecodeError:
                            continue
                            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during streaming: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            raise

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose() 