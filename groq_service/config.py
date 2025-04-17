"""
Configuration management for the Groq service.
"""
import os
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    """
    Configuration settings for the Groq service.
    Load from environment variables.
    """
    groq_api_key: SecretStr
    environment: str = "development"
    rate_limit_requests: int = 60
    rate_limit_period: int = 60
    enable_cache: bool = False
    cache_ttl: int = 3600
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_config() -> Settings:
    """
    Get the configuration settings.
    Returns:
        Settings: Configuration settings
    """
    return Settings() 