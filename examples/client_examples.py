"""
Examples of calling the Groq service from another application.
This demonstrates different ways to interact with the service.
"""
import os
import json
import asyncio
import requests
from typing import Dict, Any

# Example 1: Direct Python Package Import
async def example_direct_import():
    """Use the GroqClient directly from Python code."""
    print("\n--- Example 1: Direct Python Package Import ---")
    
    # Import the client
    from groq_service import GroqClient
    
    # Initialize client
    client = GroqClient()
    
    try:
        # Send a prompt
        prompt = "What is the capital of France?"
        print(f"Prompt: {prompt}")
        
        # Get completion
        response = await client.complete(prompt)
        print(f"Response: {response}")
    finally:
        await client.close()

# Example 2: REST API (HTTP request)
def example_rest_api():
    """Call the REST API using HTTP requests."""
    print("\n--- Example 2: REST API (HTTP request) ---")
    
    # API endpoint
    api_url = "http://localhost:8500/completions"
    
    # Prepare request
    prompt = "What is the capital of Italy?"
    payload = {
        "prompt": prompt,
        "temperature": 0.7
    }
    
    print(f"Sending POST request to {api_url}")
    print(f"Prompt: {prompt}")
    
    # Make the request
    response = requests.post(api_url, json=payload)
    
    # Parse and display response
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['text']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example 3: REST API Streaming
def example_streaming_api():
    """Call the streaming API endpoint."""
    print("\n--- Example 3: REST API Streaming ---")
    
    # API endpoint
    api_url = "http://localhost:8500/completions/stream"
    
    # Prepare request
    prompt = "List the first 5 planets in our solar system."
    payload = {
        "prompt": prompt,
        "temperature": 0.7
    }
    
    print(f"Sending streaming request to {api_url}")
    print(f"Prompt: {prompt}")
    print("Response:")
    
    # Make streaming request
    with requests.post(api_url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                # Parse the SSE format
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    print(data, end='', flush=True)
    print()

# Example 4: Command Line (subprocess)
def example_command_line():
    """Call the service using command-line interface."""
    print("\n--- Example 4: Command Line (subprocess) ---")
    
    import subprocess
    
    # Prepare command
    prompt = "What is the capital of Spain?"
    command = ["groq-service", "complete", "--json", prompt]
    
    print(f"Running command: {' '.join(command)}")
    
    # Execute command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Parse and display output
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            print(f"Response: {data['text']}")
        except json.JSONDecodeError:
            print(f"Raw output: {result.stdout}")
    else:
        print(f"Error: {result.stderr}")

async def main():
    """Run all examples."""
    # Uncomment examples to run them
    
    # Example 1: Direct Python Package Import
    await example_direct_import()
    
    # Example 2: REST API (HTTP request)
    # Note: API server must be running (groq-service serve)
    # example_rest_api()
    
    # Example 3: REST API Streaming
    # Note: API server must be running (groq-service serve)
    # example_streaming_api()
    
    # Example 4: Command Line (subprocess)
    # Note: Package must be installed (pip install -e .)
    # example_command_line()

if __name__ == "__main__":
    asyncio.run(main()) 