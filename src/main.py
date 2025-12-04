"""
Main entry point for Rock-Paper-Scissors Game
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional
import threading
import socket
import json

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules explicitly for PyInstaller
try:
    from ui import create_app
except ImportError:
    # If running as executable, modules are in the same directory
    import ui
    create_app = ui.create_app


def main():
    """Main function to start the application"""
    print("Starting Rock-Paper-Scissors Game...")
    print("=" * 50)
    print("Game Modes Available:")
    print("  • Single Player vs AI")
    print("  • Multiplayer via Wi-Fi")
    print("  • Multiplayer via Bluetooth (optional)")
    print("=" * 50)
    
    # Create and run the application
    root = create_app()
    root.mainloop()


if __name__ == "__main__":
    main()
