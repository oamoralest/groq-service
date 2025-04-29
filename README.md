# Groq Service

A Python service that provides a clean, async interface to the Groq API, with support for multiple models, streaming responses, and rate limiting.

## Features

- 🚀 Async-first design
- 🔄 Streaming support
- ⚡ Rate limiting built-in
- ⚙️ REST API with FastAPI
- 🐳 Docker containerization 
- 🖥️ Command-line interface
- 🎯 Type hints throughout
- 📝 Comprehensive logging
- 🔌 Easy integration
- 🎭 Multiple model support

## Supported Models

- `llama2-70b-4096`: Llama 2 70B
- `llama-3.3-70b-versatile`: Llama 3 70B Versatile

## Installation

### As a Python Package

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
cp .env.template .env
```

4. Install the package:
```bash
pip install -e .
```

### Using Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/groq-service.git
cd groq-service
```

2. Create a .env file with your Groq API key:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

3. Build and run the Docker container:
```bash
docker-compose up -d
```

## Usage

### As a Python Package

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

### Using the REST API

The service exposes a REST API with FastAPI that you can interact with:

1. Start the API server:
```bash
groq-service serve
```

2. Make requests to the API:
```bash
# Basic completion
curl -X POST http://localhost:8500/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'

# Streaming completion
curl -X POST http://localhost:8500/completions/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a story about a robot"}'
```

### Using the Command-Line Interface

The package includes a command-line interface for quick access:

```bash
# Basic completion
groq-service complete "What is the capital of France?"

# Streaming completion
groq-service complete --stream "Write a story about a robot"

# Output as JSON
groq-service complete --json "What is the capital of France?"
```

### Using Docker

If you're using Docker, you can access the API at `http://localhost:8500` after starting the container with `docker-compose up -d`.

## Integrating with Other Services

This service can be integrated with other applications in multiple ways:

1. **Python Package Import**: Directly import and use the GroqClient in your Python applications
2. **REST API**: Make HTTP requests to the API endpoints
3. **Docker Container**: Run as a containerized service accessible to other containers
4. **Command-Line Interface**: Use the CLI for scripting or direct interaction

## Configuration

The service can be configured using environment variables:

- `GROQ_API_KEY`: Your Groq API key
- `ENVIRONMENT`: development/test/production
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per period
- `RATE_LIMIT_PERIOD`: Time period for rate limiting in seconds
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- `API_HOST`: Host to bind the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8500)

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