"""
Command-line interface for Groq service.
"""
import sys
import argparse
import asyncio
import json
from typing import Optional

from .client import GroqClient
from .server import main as run_server

async def process_prompt(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    output_format: str = "text"
):
    """Process a prompt using the Groq service."""
    client = GroqClient()
    
    try:
        if stream:
            # Stream output
            async for chunk in client.stream(prompt, temperature, max_tokens):
                if output_format == "json":
                    print(json.dumps({"text": chunk, "finished": False}), flush=True)
                else:
                    print(chunk, end="", flush=True)
            
            if output_format == "json":
                print(json.dumps({"text": "", "finished": True}))
            else:
                print()
        else:
            # Get complete response
            response = await client.complete(prompt, temperature, max_tokens)
            
            if output_format == "json":
                print(json.dumps({
                    "text": response,
                    "model": client.model.name,
                }))
            else:
                print(response)
    finally:
        await client.close()

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Groq Service CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run server command
    server_parser = subparsers.add_parser("serve", help="Run API server")
    
    # Completion command
    complete_parser = subparsers.add_parser("complete", help="Generate a completion")
    complete_parser.add_argument("prompt", type=str, help="Prompt text")
    complete_parser.add_argument("--temperature", type=float, default=0.7, help="Temperature (0.0-1.0)")
    complete_parser.add_argument("--max-tokens", type=int, help="Maximum tokens to generate")
    complete_parser.add_argument("--stream", action="store_true", help="Stream response")
    complete_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        run_server()
    elif args.command == "complete":
        output_format = "json" if args.json else "text"
        asyncio.run(process_prompt(
            args.prompt,
            args.temperature,
            args.max_tokens,
            args.stream,
            output_format
        ))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 