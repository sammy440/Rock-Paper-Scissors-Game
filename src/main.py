"""
Main entry point for Rock-Paper-Scissors Game
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import create_app


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
