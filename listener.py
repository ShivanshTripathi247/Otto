import speech_recognition as sr

def initialize_listener():
    """
    Initializes the recognizer and pre-loads the Whisper model into memory.
    """
    print("Initializing speech recognition engine...")
    r = sr.Recognizer()
    try:
        # Create a silent, empty AudioData object to satisfy the function's requirements.
        # This is needed to correctly load the model into memory without a real audio source.
        dummy_audio = sr.AudioData(b'', 16000, 2) # 16kHz sample rate, 2 bytes/sample (16-bit)
        
        # This call will now succeed
        r.recognize_whisper(dummy_audio, model="base.en")
        
        print("Speech recognition engine is ready.")
        return True
    except Exception as e:
        print(f"Failed to initialize Whisper: {e}")
        return False

def listen_for_command():
    """
    Listens for audio via the microphone and transcribes it using the local Whisper model.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            print("Listening timed out. No command detected.")
            return None

    try:
        print("Transcribing audio...")
        text = recognizer.recognize_whisper(audio, language="english", model="base.en")
        print(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        print("Whisper could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Whisper service; {e}")
        return None