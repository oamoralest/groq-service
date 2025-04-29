FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Copy the application
COPY app.py .

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"] 