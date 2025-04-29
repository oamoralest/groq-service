"""
Example Flask application that calls the Groq Service API.
"""
import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Get the Groq service URL from environment variable or use default
GROQ_SERVICE_URL = os.getenv('GROQ_SERVICE_URL', 'http://groq-service:8000')

@app.route('/')
def index():
    """Simple HTML interface."""
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Groq Client Example</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                textarea { width: 100%; height: 100px; }
                .result { margin-top: 20px; white-space: pre-wrap; }
                button { padding: 10px 20px; }
            </style>
        </head>
        <body>
            <h1>Groq Client Example</h1>
            <form id="promptForm">
                <div>
                    <label for="prompt">Enter your prompt:</label>
                    <textarea id="prompt" name="prompt" required>What is the capital of France?</textarea>
                </div>
                <div style="margin-top: 10px">
                    <button type="submit">Submit</button>
                </div>
            </form>
            <div class="result" id="result"></div>
            
            <script>
                document.getElementById('promptForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const prompt = document.getElementById('prompt').value;
                    const resultDiv = document.getElementById('result');
                    
                    resultDiv.textContent = 'Loading...';
                    
                    try {
                        const response = await fetch('/complete', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ prompt })
                        });
                        
                        const data = await response.json();
                        resultDiv.textContent = data.text;
                    } catch (error) {
                        resultDiv.textContent = `Error: ${error.message}`;
                    }
                });
            </script>
        </body>
        </html>
    """)

@app.route('/complete', methods=['POST'])
def complete():
    """Call the Groq Service API to get a completion."""
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        # Call the Groq service API
        response = requests.post(
            f"{GROQ_SERVICE_URL}/completions",
            json={
                "prompt": prompt,
                "temperature": 0.7
            }
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the response from the Groq service
        return jsonify(response.json())
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling Groq service: {str(e)}")
        return jsonify({'error': f'Failed to get completion: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 