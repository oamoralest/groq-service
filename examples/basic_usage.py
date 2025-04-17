"""
Basic example of using the Groq service.
Shows usage of different models and features.
"""
import asyncio
import os
from dotenv import load_dotenv

# Import from the package instead of src
from groq_service.client import GroqClient

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize client with default model (llama-3.3-70b-versatile)
    client = GroqClient()
    
    try:
        # Show available models
        print("Available models:", client.available_models)
        
        # Basic completion example
        prompt = "What is the capital of France?"
        print(f"\nPrompt: {prompt}")
        response = await client.complete(prompt)
        print(f"Response: {response}\n")
        
        # Try with a different model
        client_llama2 = GroqClient("llama2-70b-4096")
        prompt = "Explain quantum computing in simple terms."
        print(f"Using Llama 2 model\nPrompt: {prompt}")
        response = await client_llama2.complete(prompt)
        print(f"Response: {response}\n")
        
        # Streaming example with custom parameters
        prompt = "Write a short story about a robot learning to paint."
        print(f"Streaming response with temperature=0.9\nPrompt: {prompt}")
        print("Response:")
        async for chunk in client.stream(prompt, temperature=0.9):
            print(chunk, end="", flush=True)
        print("\n")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close both clients
        await client.close()
        await client_llama2.close()

if __name__ == "__main__":
    asyncio.run(main()) 