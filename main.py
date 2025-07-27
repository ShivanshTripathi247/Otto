import customtkinter as ctk
import threading
import keyboard
import time
import json
import sys
import os
from llm_handler import ask_sentinel, model_exists, pull_model_with_progress
from ui_manager import StartupAnimation, CommandPalette, ResponseWindow, ListeningIndicator, ModelDownloaderWindow
from speaker import speak
from sentinel_core import SentinelCore
from listener import listen_for_command, initialize_listener
from api_handler import get_weather
from calendar_handler import get_upcoming_events


if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))



INTENT_PROMPT = """
You are a command router. Based on the user's command, what is the primary intent?
Your response must be ONLY ONE of these keywords:
wallpaper, cpu, ram, dashboard, weather, launch_app, open_website, calendar, ask.

User command: "{user_command}"
Keyword:
"""

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    sentinel = SentinelCore(main_tk_root=root)

    def handle_calendar_thread():
        """Handles the blocking calendar API call in a background thread."""
        response = get_upcoming_events()
        if response:
            # Once we have the response, schedule the UI updates to run on the main thread
            root.after(0, lambda: ResponseWindow(response_text=response))
            speak(response)

            # --- 1. Define All Handlers ---
    def process_command(command_text):
        """Uses keyword matching on AI intent to execute commands."""
        if not command_text:
            return
        
        final_prompt = INTENT_PROMPT.format(user_command=command_text)
        intent = ask_sentinel(final_prompt).lower()
        print(f"AI classified intent as: '{intent}'")

        response_text = ""

        # --- This is the key change ---
        if "calendar" in intent:
            # For the slow calendar command, start it in a thread and exit the function.
            # The thread itself will handle showing the response window.
            threading.Thread(target=handle_calendar_thread, daemon=True).start()
            return

        # --- All other fast commands are handled directly ---
        elif "wallpaper" in intent:
            sentinel.set_random_wallpaper()
            response_text = "As you wish. The wallpaper has been changed."
        elif "cpu" in intent:
            response_text = sentinel.get_cpu_usage()
        elif "ram" in intent:
            response_text = sentinel.get_ram_usage()
        elif "dashboard" in intent:
            sentinel.open_dashboard()
            response_text = "Opening the dashboard."

        # --- Commands that need a parameter ---
        elif "weather" in intent:
            param_prompt = f"From the phrase '{command_text}', what is the city name? Respond with ONLY the city name."
            city = ask_sentinel(param_prompt)
            response_text = get_weather(city) if city else "Which city's weather would you like?"

        elif "launch_app" in intent:
            param_prompt = f"From the phrase '{command_text}', what is the application name? Respond with ONLY the app name."
            app_name = ask_sentinel(param_prompt)
            response_text = sentinel.open_application(app_name) if app_name else "Which application should I launch?"

        elif "open_website" in intent:
            param_prompt = f"From the phrase '{command_text}', what is the website URL? Respond with ONLY the URL."
            url = ask_sentinel(param_prompt)
            response_text = sentinel.open_website(url) if url else "Which website should I open?"

        # --- Fallback for general questions ---
        else:
            response_text = ask_sentinel(f"The user asked: '{command_text}'. Provide a concise, helpful response.")
        
        # --- Show and speak the final response ---
        if response_text:
            root.after(0, lambda: ResponseWindow(response_text=response_text))
            speak(response_text)
                
    def handle_voice_command():
        indicator = ListeningIndicator()
        root.update()
        command = listen_for_command()
        indicator.destroy()
        if command:
            process_command(command)

    def voice_command_thread_handler():
        thread = threading.Thread(target=handle_voice_command)
        thread.daemon = True
        thread.start()
        
    def open_command_palette_ui():
        palette = CommandPalette(command_handler_func=process_command)

    # --- 2. Set up Both Global Hotkeys ---
    keyboard.add_hotkey('ctrl+space', lambda: root.after(0, open_command_palette_ui))
    keyboard.add_hotkey('ctrl+alt+space', voice_command_thread_handler)
    print("Hotkeys registered: 'Ctrl+Space' for text, 'Ctrl+Alt+Space' for voice.")
    
    # --- 3. Pre-load the Whisper model ---
    init_thread = threading.Thread(target=initialize_listener)
    init_thread.daemon = True
    init_thread.start()
    
    # --- 4. Start Tray Icon ---
    tray_thread = threading.Thread(target=sentinel.run_background_tasks)
    tray_thread.daemon = True
    tray_thread.start()
    
    # --- 5. Run Startup Sequence ---
    greeting = ask_sentinel(f"Generate a short, futuristic greeting. It is currently {time.strftime('%I:%M %p')} on a {time.strftime('%A')}.")    
    startup_app = StartupAnimation(text_to_display=greeting)

    print("Startup sequence complete. Sentinel is ready.")
    root.mainloop()

    def start_full_app():
        """Contains the logic to start the main application after setup."""
        keyboard.add_hotkey('ctrl+space', lambda: root.after(0, open_command_palette_ui))
        keyboard.add_hotkey('ctrl+alt+space', voice_command_thread_handler)
        print("Hotkeys registered.")

        threading.Thread(target=initialize_listener, daemon=True).start()
        threading.Thread(target=sentinel.run_background_tasks, daemon=True).start()
        
        greeting = ask_sentinel(f"Generate a very short, futuristic greeting (NOT MORE THAN 20 WORDS). It is currently {time.strftime('%I:%M %p')} on a {time.strftime('%A')}.")
        startup_app = StartupAnimation(text_to_display=greeting)
        print("Startup sequence complete. Sentinel is ready.")

    # --- New Startup Logic ---
    if not model_exists():
        downloader_window = ModelDownloaderWindow()
        def update_dl_status(text):
            root.after(0, downloader_window.update_status, text)
        def on_dl_complete():
            root.after(0, downloader_window.destroy)
            start_full_app()
        threading.Thread(target=pull_model_with_progress, args=("phi3", update_dl_status, on_dl_complete), daemon=True).start()
    else:
        print("AI model 'phi3' is ready.")
        start_full_app()

    root.mainloop()