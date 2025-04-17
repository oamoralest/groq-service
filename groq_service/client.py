"""
Groq API client implementation.
"""
import asyncio
import logging
from typing import AsyncGenerator, Optional

from groq import AsyncGroq
from .models.groq_model import GroqModel
from .config import get_config

class GroqClient:
    """
    Async client for interacting with Groq's API.
    Handles rate limiting, model management, and API interactions.
    """
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.config = get_config()
        self.model = GroqModel(model_name)
        
        # Configure logging
        logging.basicConfig(level=self.config.log_level)
        self.logger = logging.getLogger(__name__)
        
        # Initialize Groq client
        self.client = AsyncGroq(
            api_key=self.config.groq_api_key.get_secret_value(),
        )
        
        # Rate limiting state
        self._request_times = []
        self._rate_limit_lock = asyncio.Lock()
    
    @property
    def available_models(self) -> list[str]:
        """Get list of available models."""
        return ["llama-3.3-70b-versatile"]
    
    async def _check_rate_limit(self):
        """
        Check and enforce rate limiting.
        Waits if necessary to stay within limits.
        """
        async with self._rate_limit_lock:
            now = asyncio.get_event_loop().time()
            
            # Remove old requests from tracking
            cutoff = now - self.config.rate_limit_period
            self._request_times = [t for t in self._request_times if t > cutoff]
            
            # If at limit, wait until oldest request expires
            if len(self._request_times) >= self.config.rate_limit_requests:
                wait_time = self._request_times[0] - cutoff
                self.logger.debug(f"Rate limit reached, waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
            
            # Record this request
            self._request_times.append(now)
    
    async def complete(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt: The input text to complete
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            The generated completion text
        """
        await self._check_rate_limit()
        
        self.logger.debug(f"Sending completion request for prompt: {prompt[:50]}...")
        
        response = await self.client.chat.completions.create(
            model=self.model.name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.choices[0].message.content
    
    async def stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a completion for the given prompt.
        
        Args:
            prompt: The input text to complete
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            
        Yields:
            Generated text chunks as they become available
        """
        await self._check_rate_limit()
        
        self.logger.debug(f"Starting streaming request for prompt: {prompt[:50]}...")
        
        stream = await self.client.chat.completions.create(
            model=self.model.name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    
    async def close(self):
        """Close the client and cleanup resources."""
        # Currently a no-op as AsyncGroq doesn't require explicit cleanup
        pass 