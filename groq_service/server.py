"""
Server entry point for running the Groq service API.
"""
import os
import logging
import uvicorn
from dotenv import load_dotenv

from .config import get_config

# Load environment variables
load_dotenv()

def main():
    """Run the API server."""
    config = get_config()
    
    # Configure logging
    logging.basicConfig(level=config.log_level)
    logger = logging.getLogger(__name__)
    
    # Get configuration from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting Groq service API on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        "groq_service.api:app",
        host=host,
        port=port,
        reload=config.environment == "development",
        log_level=config.log_level.lower(),
    )

if __name__ == "__main__":
    main() 