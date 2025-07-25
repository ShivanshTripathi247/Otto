import pystray
from PIL import Image
import ctypes
import random
from pathlib import Path
import psutil

class SentinelCore:
    def __init__(self, main_tk_root):
        self.root = main_tk_root
        self.current_wallpaper = None

    def set_wallpaper(self, image_path):
        """Sets the desktop wallpaper and updates the tracker."""
        absolute_path = image_path.resolve()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(absolute_path), 3)
        print(f"Wallpaper changed to: {image_path.name}")
        self.current_wallpaper = image_path

    def set_random_wallpaper(self):
        """Picks a random wallpaper that is different from the current one."""
        wallpaper_dir = Path("assets/wallpapers")
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
        """Stops the tray icon and quits the main application."""
        icon.stop()
        self.root.quit()

    def run_background_tasks(self):
        """Creates and runs the system tray icon."""
        try:
            image = Image.open("assets/icon.png")
        except FileNotFoundError:
            image = Image.new('RGB', (64, 64), color='black')
        
        menu = (
            pystray.MenuItem('Set New Wallpaper', self.set_random_wallpaper),
            pystray.MenuItem('Exit', self.on_exit_clicked)
        )
        
        # The order of arguments is now correct: name, icon, title, menu
        icon = pystray.Icon("Sentinel", image, "Sentinel Assistant", menu)
        icon.run()

    # Add these two methods inside the SentinelCore class in sentinel_core.py

    def get_cpu_usage(self):
        """Returns the current CPU usage as a percentage."""
        # The interval allows the system to get a more accurate reading
        usage = psutil.cpu_percent(interval=1)
        return f"Current CPU load is at {usage} percent."

    def get_ram_usage(self):
        """Returns the current RAM usage as a percentage."""
        usage = psutil.virtual_memory().percent
        return f"Current memory usage is at {usage} percent."