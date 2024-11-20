# main.py
import os
import sys
from pathlib import Path
from kivy.resources import resource_add_path
from kivy.logger import Logger

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.core.app import MainApp
    from src.utils.logger import app_logger
except ImportError as e:
    print(f"Failed to import modules: {e}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        app_logger.info("Starting application...")
        app = MainApp()
        app.run()
    except Exception as e:
        app_logger.critical(f"Application failed to start: {str(e)}")
        sys.exit(1)