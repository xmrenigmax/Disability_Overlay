# src/__init__.py
import os
import sys
from pathlib import Path

# Add package root to Python path
package_root = Path(__file__).parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))