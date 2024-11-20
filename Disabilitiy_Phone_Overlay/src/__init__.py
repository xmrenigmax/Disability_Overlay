# src/__init__.py
import os
from pathlib import Path
import sys

# Add src directory to Python path
SRC_DIR = Path(__file__).parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))