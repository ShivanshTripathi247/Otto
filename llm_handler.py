import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def ask_sentinel(prompt):
    """Sends a prompt to the local Ollama server and gets a response."""
    payload = {
        "model": "phi3",  # Updated with your fix!
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        full_response = response.json()['response']

        # Simple trick to remove the AI's "explanation" part if it exists
        # It splits the text by the first newline and takes only the first line.
        greeting_only = full_response.strip().split('\n')[0]

        return greeting_only

    except requests.exceptions.RequestException:
        # Return a default greeting if the AI is offline
        return "Welcome back. All systems operational."