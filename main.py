#!/usr/bin/env python
"""
Utility Token Generation Project - Main Entry Point

This script serves as the main entry point for the Utility Token Generation project.
It launches the GUI interface by default or allows command-line selection of components.
"""

import os
import sys
import argparse

# Ensure the src directory is in the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

def print_help():
    """Print usage information."""
    print("Utility Token Generation Project")
    print("--------------------------------")
    print("Usage:")
    print("  python main.py [component]")
    print("")
    print("Available components:")
    print("  token       - Generate a token")
    print("  key         - Generate a decoder key")
    print("  decrypt     - Decrypt a token")
    print("  clean       - Process raw token data")
    print("  visualize   - Visualize token data")
    print("  test        - Run component tests")
    print("  gui         - Launch GUI interface (default)")
    print("")
    print("Examples:")
    print("  python main.py token     # Run token generator")
    print("  python main.py gui       # Launch GUI interface")
    print("  python main.py           # Launch GUI interface (default)")

def run_component(component):
    """Run the specified component."""
    if component == "token":
        from src.Token import main as token_main
        token_main()
    
    elif component == "key":
        from src.DKGA02 import main as dkga_main
        dkga_main()
    
    elif component == "decrypt":
        from src.TokenDecrypter import main as decrypt_main
        decrypt_main()
    
    elif component == "clean":
        from src.data_cleaning import main as clean_main
        clean_main()
    
    elif component == "visualize":
        from src.TokenVisualizer import main as visualize_main
        visualize_main()
    
    elif component == "test":
        from src.test_components import main as test_main
        test_main()
    
    elif component == "gui":
        # Import here to avoid circular imports
        import tkinter as tk
        from src.UtilityTokenGUI import UtilityTokenApp
        # Launch GUI
        root = tk.Tk()
        app = UtilityTokenApp(root)
        root.mainloop()
    
    else:
        print_help()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Utility Token Generation Project", add_help=False)
    parser.add_argument('component', nargs='?', default='gui', 
                        help='Component to run (token, key, decrypt, clean, visualize, test, gui)')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    if args.help:
        print_help()
        return
    
    run_component(args.component)

if __name__ == "__main__":
    main()
