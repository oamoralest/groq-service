"""
Rate limiting implementation for the Groq service.
Provides async-compatible rate limiting with configurable windows.
"""
import asyncio
import time
from typing import Dict, Optional
from dataclasses import dataclass

from ..config import get_config
from .logger import logger

@dataclass
class TokenBucket:
    """Token bucket implementation for rate limiting."""
    capacity: int
    fill_rate: float
    tokens: float = 0.0
    last_update: float = time.time()

    def update_tokens(self) -> None:
        """Update the number of tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        new_tokens = elapsed * self.fill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_update = now

    async def acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens from the bucket.
        
        Args:
            tokens: Number of tokens to acquire
            
        Returns:
            True if tokens were acquired, False otherwise
        """
        self.update_tokens()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

class RateLimiter:
    """Async-compatible rate limiter using token bucket algorithm."""
    def __init__(self):
        config = get_config()
        self.buckets: Dict[str, TokenBucket] = {}
        self.requests_per_period = config.RATE_LIMIT_REQUESTS
        self.period_seconds = config.RATE_LIMIT_PERIOD
        self.fill_rate = self.requests_per_period / self.period_seconds

    def get_bucket(self, key: str) -> TokenBucket:
        """Get or create a token bucket for the given key."""
        if key not in self.buckets:
            self.buckets[key] = TokenBucket(
                capacity=self.requests_per_period,
                fill_rate=self.fill_rate,
                tokens=self.requests_per_period
            )
        return self.buckets[key]

    async def acquire(self, key: str, tokens: int = 1, wait: bool = True) -> bool:
        """
        Attempt to acquire tokens for the given key.
        
        Args:
            key: The rate limiting key (e.g., API endpoint)
            tokens: Number of tokens to acquire
            wait: Whether to wait for tokens to become available
            
        Returns:
            True if tokens were acquired, False otherwise
        """
        bucket = self.get_bucket(key)
        
        if wait:
            while not await bucket.acquire(tokens):
                await asyncio.sleep(0.1)
            return True
        
        return await bucket.acquire(tokens)

# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter 