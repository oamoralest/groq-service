"""
Groq model implementation.
"""

class GroqModel:
    """
    Represents a Groq model with its configuration and capabilities.
    """
    
    def __init__(self, name: str):
        """
        Initialize a Groq model.
        
        Args:
            name: Name of the model to use
        """
        if name not in ["llama2-70b-4096", "llama-3.3-70b-versatile"]:
            raise ValueError(
                f"Invalid model name: {name}. "
                "Available models: llama2-70b-4096, llama-3.3-70b-versatile"
            )
        self.name = name

    def _create_messages(self, prompt: str) -> List[Dict[str, str]]:
        """Convert prompt to messages format."""
        return [{"role": "user", "content": prompt}]

    async def complete(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> ModelResponse:
        """Generate a completion for the given prompt."""
        parameters = self._validate_parameters(parameters)
        messages = self._create_messages(prompt)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("completion")
        
        try:
            response: ChatCompletion = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=messages,
                model=self.name,
                temperature=parameters.temperature,
                max_tokens=parameters.max_tokens,
                top_p=parameters.top_p,
                stream=False
            )
            
            return ModelResponse(
                text=response.choices[0].message.content,
                finish_reason=response.choices[0].finish_reason,
                model=self.name,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"Error during completion: {str(e)}")
            raise

    async def stream(
        self,
        prompt: str,
        parameters: Optional[ModelParameters] = None
    ) -> AsyncGenerator[str, None]:
        """Stream completions for the given prompt."""
        parameters = self._validate_parameters(parameters)
        messages = self._create_messages(prompt)
        
        # Apply rate limiting
        await self.rate_limiter.acquire("stream")
        
        try:
            # Create streaming response
            stream = await asyncio.to_thread(
                self.client.chat.completions.create,
                messages=messages,
                model=self.name,
                temperature=parameters.temperature,
                max_tokens=parameters.max_tokens,
                top_p=parameters.top_p,
                stream=True
            )
            
            async for chunk in self._async_iterate(stream):
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            raise

    async def _async_iterate(self, stream):
        """Convert sync iterator to async iterator."""
        for item in stream:
            yield item
            await asyncio.sleep(0)  # Allow other tasks to run

    async def close(self) -> None:
        """Clean up resources."""
        # No cleanup needed for official client
        pass 