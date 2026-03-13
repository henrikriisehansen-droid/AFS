import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController

if __name__ == "__main__":
    app_controller = MainController()
    app_controller.run()
