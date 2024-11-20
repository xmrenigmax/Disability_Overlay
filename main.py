# main.py
import os
import sys
from pathlib import Path
from kivy.resources import resource_add_path
from kivy.logger import Logger

# Get absolute path to src directory
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / 'src'

# Add src to Python path if not already there
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Now we can import our modules using relative imports
try:
    from src.core.app import MainApp
    from src.utils.logger import app_logger
except ImportError as e:
    print(f"Failed to import modules: {e}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

def main():
    """
    Application entry point with error handling and resource management
    """
    try:
        # Configure resource paths
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
            
        # Initialize and run application
        app_logger.info("Starting application...")
        app = MainApp()
        app.run()
        
    except Exception as e:
        app_logger.critical(f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()