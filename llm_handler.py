import requests
import json
import subprocess

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def is_server_running():
    """Checks if the Ollama server is running and accessible."""
    try:
        response = requests.get(OLLAMA_URL.replace("/api/generate", "/"), timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def model_exists(model_name="phi3"):
    """Quickly checks if the model is already installed."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return model_name in result.stdout
    except Exception:
        return False

def ask_sentinel(prompt):
    """Sends a prompt to the local Ollama server and gets a response."""
    payload = {"model": "phi3", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        full_response = response.json()['response']
        return full_response.strip().split('\n')[0]
    except requests.exceptions.RequestException:
        return "Welcome back. All systems operational."
