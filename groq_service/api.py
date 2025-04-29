"""
REST API for Groq service using FastAPI.
"""
import logging
from typing import List, Optional, Dict, Any, AsyncGenerator
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .client import GroqClient
from .config import get_config

# Initialize logging
config = get_config()
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Groq Service API",
    description="API for interacting with Groq's LLM models",
    version="0.1.0",
)

# Input/output models
class CompletionRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None

class CompletionResponse(BaseModel):
    text: str
    model: str

# Client dependency
async def get_client():
    client = GroqClient()
    try:
        yield client
    finally:
        await client.close()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "groq-service"}

@app.get("/models")
async def list_models(client: GroqClient = Depends(get_client)) -> List[str]:
    """Get available models."""
    return client.available_models

@app.post("/completions")
async def create_completion(
    request: CompletionRequest,
    client: GroqClient = Depends(get_client)
) -> CompletionResponse:
    """Generate a completion for the given prompt."""
    try:
        response = await client.complete(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return CompletionResponse(
            text=response,
            model=client.model.name,
        )
    except Exception as e:
        logger.error(f"Error in completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_stream(client: GroqClient, request: CompletionRequest):
    """Generate and yield streaming response chunks."""
    try:
        async for chunk in client.stream(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        ):
            yield f"data: {chunk}\n\n"
    except Exception as e:
        logger.error(f"Error in stream: {str(e)}")
        yield f"data: [ERROR] {str(e)}\n\n"
    finally:
        yield "data: [DONE]\n\n"

@app.post("/completions/stream")
async def create_streaming_completion(
    request: CompletionRequest,
    client: GroqClient = Depends(get_client)
):
    """Stream a completion for the given prompt."""
    return StreamingResponse(
        generate_stream(client, request),
        media_type="text/event-stream"
    ) 