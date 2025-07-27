import pystray
from PIL import Image
import ctypes
import random
from pathlib import Path
import psutil
import webbrowser
import os
import sys
from dashboard_ui import DashboardWindow

# This block determines the correct base path for assets
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class SentinelCore:
    def __init__(self, main_tk_root):
        self.root = main_tk_root
        self.current_wallpaper = None
        self.dashboard_window = None 

    def open_application(self, app_name):
        try:
            os.startfile(app_name)
            return f"Opening {app_name}..."
        except Exception as e:
            print(f"Error opening application: {e}")
            return f"Sorry, I could not find or open {app_name}."

    def open_website(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            webbrowser.open(url, new=2)
            return f"Opening {url} in your browser."
        except Exception as e:
            print(f"Error opening website: {e}")
            return "Sorry, there was an error opening the website."

    def _create_dashboard_window(self):
        self.dashboard_window = DashboardWindow(sentinel_instance=self)

    def open_dashboard(self):
        if self.dashboard_window is None or not self.dashboard_window.winfo_exists():
            self.root.after(0, self._create_dashboard_window)
        else:
            self.dashboard_window.focus()

    def set_wallpaper(self, image_path):
        absolute_path = image_path.resolve()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(absolute_path), 3)
        print(f"Wallpaper changed to: {image_path.name}")
        self.current_wallpaper = image_path

    def set_random_wallpaper(self):
        # Use BASE_PATH to find the wallpapers directory reliably
        wallpaper_dir = Path(os.path.join(BASE_PATH, 'assets', 'wallpapers'))
        images = list(wallpaper_dir.glob("*.jpg")) + list(wallpaper_dir.glob("*.png"))

        if not images:
            print("No wallpapers found.")
            return

        if len(images) == 1:
            self.set_wallpaper(images[0])
            return

        possible_choices = [img for img in images if img != self.current_wallpaper]
        if not possible_choices:
            possible_choices = images

        new_wallpaper = random.choice(possible_choices)
        self.set_wallpaper(new_wallpaper)

    def on_exit_clicked(self, icon, item):
        icon.stop()
        self.root.quit()

    def run_background_tasks(self):
        try:
            # Use BASE_PATH to find the icon reliably
            icon_path = os.path.join(BASE_PATH, 'assets', 'icon.ico')
            image = Image.open(icon_path)
        except FileNotFoundError:
            image = Image.new('RGB', (64, 64), color='black')
        
        menu = (
            pystray.MenuItem('Dashboard', self.open_dashboard),
            pystray.MenuItem('Set New Wallpaper', self.set_random_wallpaper),
            pystray.MenuItem('Exit', self.on_exit_clicked)
        )
        
        icon = pystray.Icon("Otto", image, "Otto Assistant", menu)
        icon.run()

    def get_cpu_usage(self):
        usage = psutil.cpu_percent(interval=1)
        return f"Current CPU load is at {usage} percent."

    def get_ram_usage(self):
        usage = psutil.virtual_memory().percent
        return f"Current memory usage is at {usage} percent."