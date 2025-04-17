# Groq Service

A Python service that provides a clean, async interface to the Groq API, with support for multiple models, streaming responses, and rate limiting.

## Features

- 🚀 Async-first design
- 🔄 Streaming support
- ⚡ Rate limiting built-in
- 🎯 Type hints throughout
- 📝 Comprehensive logging
- 🔌 Easy integration
- 🎭 Multiple model support

## Supported Models

- `llama2-70b-4096`: Llama 2 70B
- `llama-3.3-70b-versatile`: Llama 3 70B Versatile

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/groq-service.git
cd groq-service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example environment file and fill in your Groq API key:
```bash
cp .env.example .env
```

## Usage

Here's a simple example of how to use the service:

```python
import asyncio
from groq_service import GroqClient

async def main():
    # Initialize client
    client = GroqClient()
    
    try:
        # Basic completion
        response = await client.complete("What is the capital of France?")
        print(f"Response: {response}")
        
        # Streaming example
        async for chunk in client.stream("Write a story about a robot"):
            print(chunk, end="", flush=True)
            
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Check the `examples` directory for more usage examples.

## Configuration

The service can be configured using environment variables:

- `GROQ_API_KEY`: Your Groq API key
- `ENVIRONMENT`: development/test/production
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per period
- `RATE_LIMIT_PERIOD`: Time period for rate limiting in seconds
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
pytest
```

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 