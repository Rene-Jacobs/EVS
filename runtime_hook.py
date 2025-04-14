
import os
import sys

# Handle both frozen and non-frozen environments
if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    base_dir = sys._MEIPASS
else:
    # Running in normal Python environment
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add base directory to path
sys.path.insert(0, base_dir)
