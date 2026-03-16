import threading
import pystray
from PIL import Image, ImageDraw
import ctypes
import sys

# Windows API constants
SW_HIDE = 0
SW_SHOW = 5

def get_console_window():
    return ctypes.windll.kernel32.GetConsoleWindow()

def create_image():
    # Generate a simple icon image
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (16, 16, 48, 48),
        fill=(0, 255, 128)
    )
    return image

class TrayManager:
    def __init__(self):
        self.icon = None

    def show_window(self, icon, item):
        hwnd = get_console_window()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
        if self.icon:
            self.icon.stop()

    def exit_app(self, icon, item):
        if self.icon:
            self.icon.stop()
        sys.exit(0)

    def minimize_to_tray(self):
        hwnd = get_console_window()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
        
        menu = pystray.Menu(
            pystray.MenuItem("Restore", self.show_window),
            pystray.MenuItem("Exit", self.exit_app)
        )
        self.icon = pystray.Icon("Cindy", create_image(), "Cindy Assistant", menu)
        
        # Run the tray icon loop in a separate thread to avoid blocking main program
        threading.Thread(target=self.icon.run, daemon=True).start()

# Global tray manager instance
tray_manager = TrayManager()

def run_in_background():
    tray_manager.minimize_to_tray()
