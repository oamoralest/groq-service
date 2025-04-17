"""
Configuration management for the Groq service.
Handles environment variables, API keys, and environment-specific settings.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseSettings, SecretStr

class Environment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"

class GroqConfig(BaseSettings):
    # API Configuration
    GROQ_API_KEY: SecretStr
    GROQ_API_BASE_URL: str = "https://api.groq.com/v1"
    
    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_PERIOD: int = 60  # in seconds
    
    # Caching
    ENABLE_CACHE: bool = False
    CACHE_TTL: int = 3600  # in seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == Environment.TEST

# Global config instance
config: Optional[GroqConfig] = None

def get_config() -> GroqConfig:
    """
    Get the global configuration instance.
    Creates a new instance if one doesn't exist.
    """
    global config
    if config is None:
        config = GroqConfig()
    return config 