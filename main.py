import sys
import os

# Resolve the root directory for both development and frozen execution
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # PyInstaller internal bundle directory
    bundle_dir = sys._MEIPASS
    sys.path.append(bundle_dir)
else:
    # Local development directory
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(bundle_dir)

import flet as ft
from controllers.main_controller import MainController

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "AFS - Validator"
        page.theme_mode = ft.ThemeMode.DARK
        page.window_width = 1300
        page.window_height = 900
        page.bgcolor = "#010409" # GitHub dark background
        page.padding = 20
        
        # Use a modern font if possible (Flet handles system fonts well)
        page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE,
        )
        
        try:
            app_controller = MainController(page)
            app_controller.run()
        except Exception as e:
            # If frozen and windowed, errors might be invisible. 
            # Attempt to write to a log file in the user's home directory.
            log_path = os.path.expanduser("~/AFS-Validator-error.log")
            with open(log_path, "a") as f:
                import traceback
                f.write(f"\n--- Crash at {os.popen('date').read().strip()} ---\n")
                traceback.print_exc(file=f)
            raise e

    ft.app(target=main)
