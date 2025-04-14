import os
import sys
import importlib.util


def add_to_path():
    # Get the base directory
    if getattr(sys, "frozen", False):
        # Running in PyInstaller bundle
        base_dir = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add src directory to path
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    # Add base directory to path
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
