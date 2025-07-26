import customtkinter as ctk
import threading
from speaker import speak # We'll add voice feedback for the launcher

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, sentinel_instance):
        super().__init__()
        
        self.sentinel = sentinel_instance

        self.title("Sentinel Dashboard")
        self.geometry("400x420")
        self.resizable(False, False)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Live System Stats Section ---
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(stats_frame, text="Live System Stats", font=("Roboto", 14, "bold")).pack()
        self.cpu_label = ctk.CTkLabel(stats_frame, text="CPU: -- %")
        self.cpu_label.pack(fill="x", padx=10)
        self.ram_label = ctk.CTkLabel(stats_frame, text="RAM: -- %")
        self.ram_label.pack(fill="x", padx=10)

        # --- Launcher Section ---
        launcher_frame = ctk.CTkFrame(main_frame)
        launcher_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(launcher_frame, text="Launcher", font=("Roboto", 14, "bold")).pack()
        self.launcher_entry = ctk.CTkEntry(launcher_frame, placeholder_text="e.g., notepad or google.com")
        self.launcher_entry.pack(fill="x", pady=5)
        
        button_frame = ctk.CTkFrame(launcher_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        ctk.CTkButton(button_frame, text="Launch App", command=self.on_launch_app).pack(side="left", expand=True, padx=2)
        ctk.CTkButton(button_frame, text="Open Website", command=self.on_open_website).pack(side="right", expand=True, padx=2)

        # Start the live update loop
        self.update_stats_live()

    def update_stats_live(self):
        """Periodically updates the CPU and RAM labels."""
        cpu_stat = self.sentinel.get_cpu_usage()
        ram_stat = self.sentinel.get_ram_usage()
        self.cpu_label.configure(text=cpu_stat)
        self.ram_label.configure(text=ram_stat)
        
        # Schedule this function to run again after 2 seconds (2000 ms)
        self.after(2000, self.update_stats_live)

    def on_launch_app(self):
        app_name = self.launcher_entry.get()
        if app_name:
            response = self.sentinel.open_application(app_name)
            speak(response)

    def on_open_website(self):
        url = self.launcher_entry.get()
        if url:
            response = self.sentinel.open_website(url)
            speak(response)