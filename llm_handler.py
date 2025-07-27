import requests
import json
import subprocess # Add this import

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def model_exists(model_name="phi3"):
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return model_name in result.stdout
    except Exception:
        return False

def pull_model_with_progress(model_name="phi3", status_callback=None, completion_callback=None):
    try:
        command = ['ollama', 'pull', model_name]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW)
        for line in iter(process.stdout.readline, ''):
            clean_line = line.strip().replace('⠋', '').replace('pulling manifest', 'Connecting...')
            if status_callback:
                status_callback(clean_line)
        process.stdout.close()
        process.wait()
    except Exception as e:
        if status_callback:
            status_callback(f"An error occurred: {e}")
    if completion_callback:
        completion_callback()

def ask_sentinel(prompt):
    payload = {"model": "phi3", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        full_response = response.json()['response']
        return full_response.strip().split('\n')[0]
    except requests.exceptions.RequestException:
        return "Welcome back. All systems operational."