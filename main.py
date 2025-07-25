import customtkinter as ctk
import threading
import keyboard
import time
from llm_handler import ask_sentinel
from ui_manager import StartupAnimation, CommandPalette, ResponseWindow, ListeningIndicator
from speaker import speak
from sentinel_core import SentinelCore
from listener import listen_for_command, initialize_listener

INTENT_PROMPT = """
You are a command router. Based on the user's command, identify the correct tool to use.
Your response must be ONLY one of the following tool names:
[tool_wallpaper] - If the user wants to change their wallpaper, background, or desktop image.
[tool_cpu] - If the user asks about CPU load, usage, or processor performance.
[tool_ram] - If the user asks about RAM, memory usage, or performance.
[tool_ask] - For any other general question, conversation, or request.

User command: "{user_command}"
Tool:
"""

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    sentinel = SentinelCore(main_tk_root=root)

    # --- 1. Define All Handlers ---
    def process_command(command_text):
        if not command_text:
            return
        final_prompt = INTENT_PROMPT.format(user_command=command_text)
        intent = ask_sentinel(final_prompt).lower()
        print(f"AI classified intent as: '{intent}'")
        response_text = ""
        if "wallpaper" in intent:
            sentinel.set_random_wallpaper()
            response_text = "As you wish. The wallpaper has been changed."
        elif "cpu" in intent:
            response_text = sentinel.get_cpu_usage()
        elif "ram" in intent:
            response_text = sentinel.get_ram_usage()
        else:
            response_text = ask_sentinel(f"The user asked: '{command_text}'. Provide a concise response.")
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