FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY groq_service/ ./groq_service/
COPY pyproject.toml .

# Install the package
RUN pip install -e .

# Expose the API port
EXPOSE 8500

# Set environment variables
ENV API_HOST=0.0.0.0
ENV API_PORT=8500
ENV PYTHONUNBUFFERED=1

# Run the service
CMD ["groq-service", "serve"] 