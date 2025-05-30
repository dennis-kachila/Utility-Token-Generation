#!/usr/bin/env python
"""
Test script to verify the GUI functionality
"""

import os
import sys
import tkinter as tk

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.UtilityTokenGUI import UtilityTokenApp

def main():
    """Launch the GUI for testing."""
    print("Starting GUI test...")
    # Set up high DPI awareness for Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass  # Not on Windows or not supported
    
    root = tk.Tk()
    root.title("Utility Token Generator - TEST")
    
    # Center the window on screen
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = UtilityTokenApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
