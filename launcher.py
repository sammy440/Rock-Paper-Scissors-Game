"""
Standalone launcher for Rock-Paper-Scissors Game
This file includes all necessary imports for PyInstaller
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import socket
import json
import random
import sys
import os

# Game Logic
class GameLogic:
    """Core game logic for Rock-Paper-Scissors"""
    
    MOVES = ["Rock", "Paper", "Scissors"]
    WINS = {
        "Rock": "Scissors",
        "Scissors": "Paper",
        "Paper": "Rock"
    }
    
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.history = []
    
    def get_computer_move(self):
        return random.choice(self.MOVES)
    
    def decide_winner(self, player_move, opponent_move):
        if player_move == opponent_move:
            return "tie"
        if self.WINS[player_move] == opponent_move:
            return "player1"
        return "player2"
    
    def play_round(self, player_move, computer_move=None):
        if computer_move is None:
            computer_move = self.get_computer_move()
        
        result = self.decide_winner(player_move, computer_move)
        
        if result == "player1":
            self.player_score += 1
            message = f"You Win! {player_move} beats {computer_move}"
        elif result == "player2":
            self.computer_score += 1
            message = f"You Lose! {computer_move} beats {player_move}"
        else:
            message = f"It's a Tie! Both chose {player_move}"
        
        self.rounds_played += 1
        self.history.append({
            "round": self.rounds_played,
            "player_move": player_move,
            "computer_move": computer_move,
            "result": result
        })
        
        return computer_move, result, message
    
    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.history = []
    
    def get_scores(self):
        return self.player_score, self.computer_score, self.rounds_played


# Utility functions
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def create_message(msg_type, **kwargs):
    message = {"type": msg_type, **kwargs}
    return json.dumps(message)

def parse_message(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


# Import UI from the src directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)

try:
    from ui import create_app
except ImportError:
    print("Error: Could not import UI module")
    print("Running in standalone mode - UI will be created inline")
    
    # If ui.py can't be imported, we'll need to run the Python script directly
    # For now, show an error
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Import Error",
        "Could not load game modules.\n\n"
        "Please run the game using:\n"
        "python src/main.py"
    )
    sys.exit(1)


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
