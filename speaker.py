import pyttsx3
import threading

# We no longer create a global engine instance here.

def say_text(text_to_speak):
    """
    Initializes a new TTS engine instance for each speech act.
    This is more reliable than using a single, long-lived engine.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 190)
        engine.say(text_to_speak)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS engine: {e}")

def speak(text):
    """Speaks the given text in a separate thread to avoid blocking the UI."""
    # Check if another speech thread is already running.
    if not any(t.name == 'tts_thread' for t in threading.enumerate()):
        thread = threading.Thread(target=say_text, args=(text,), name='tts_thread')
        thread.daemon = True
        thread.start()