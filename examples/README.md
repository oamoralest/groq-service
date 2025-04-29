# Groq Service Examples

This directory contains various examples of how to use the Groq Service in different scenarios.

## Example Files

- `basic_usage.py`: Simple Python script showing basic usage of the GroqClient
- `client_examples.py`: Demonstrates multiple methods of calling the service (Python, REST API, CLI)
- `docker-compose-integration.yml`: Shows how to integrate with other services using Docker

## Example App

The `example-app` directory contains a simple Flask application that demonstrates how to call the Groq Service API from another application:

- `app.py`: A Flask web application with a simple UI for sending prompts
- `Dockerfile`: Container definition for the example app
- `requirements.txt`: Python dependencies

## Running the Examples

### Basic Usage

```bash
# Make sure you have the .env file with your GROQ_API_KEY
python basic_usage.py
```

### Client Examples

```bash
# Direct import example (requires package installation)
python client_examples.py

# To run the API examples, you'll need to start the server first:
# In one terminal:
groq-service serve

# In another terminal, uncomment the API examples in the script and run:
python client_examples.py
```

### Docker Integration Example

The Docker integration example shows how to run the Groq Service alongside a Flask application:

```bash
# Navigate to the examples directory
cd examples

# Make sure your GROQ_API_KEY is in your environment
export GROQ_API_KEY=your_groq_api_key_here

# Start the services
docker-compose -f docker-compose-integration.yml up -d

# The example app will be available at http://localhost:8080
``` 