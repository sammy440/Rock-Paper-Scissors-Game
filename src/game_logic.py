"""
Game logic for Rock-Paper-Scissors
Handles game rules, winner determination, and scoring
"""

import random
from typing import Literal, Tuple

Move = Literal["Rock", "Paper", "Scissors"]
Result = Literal["player1", "player2", "tie"]


class GameLogic:
    """Core game logic for Rock-Paper-Scissors"""
    
    MOVES = ["Rock", "Paper", "Scissors"]
    
    # Define what each move beats
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
    
    def get_computer_move(self) -> Move:
        """Generate a random move for the computer"""
        return random.choice(self.MOVES)
    
    def decide_winner(self, player_move: Move, opponent_move: Move) -> Result:
        """
        Determine the winner between two moves
        
        Args:
            player_move: The player's move
            opponent_move: The opponent's move
            
        Returns:
            "player1" if player wins, "player2" if opponent wins, "tie" if draw
        """
        if player_move == opponent_move:
            return "tie"
        
        if self.WINS[player_move] == opponent_move:
            return "player1"
        
        return "player2"
    
    def play_round(self, player_move: Move, computer_move: Move = None) -> Tuple[Move, Result, str]:
        """
        Play a single round of the game
        
        Args:
            player_move: The player's chosen move
            computer_move: Optional computer move (if None, will be randomly generated)
            
        Returns:
            Tuple of (computer_move, result, message)
        """
        if computer_move is None:
            computer_move = self.get_computer_move()
        
        result = self.decide_winner(player_move, computer_move)
        
        # Update scores
        if result == "player1":
            self.player_score += 1
            message = f"You Win! {player_move} beats {computer_move}"
        elif result == "player2":
            self.computer_score += 1
            message = f"You Lose! {computer_move} beats {player_move}"
        else:
            message = f"It's a Tie! Both chose {player_move}"
        
        self.rounds_played += 1
        
        # Store in history
        self.history.append({
            "round": self.rounds_played,
            "player_move": player_move,
            "computer_move": computer_move,
            "result": result
        })
        
        return computer_move, result, message
    
    def reset_scores(self):
        """Reset all scores and history"""
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.history = []
    
    def reset_round(self):
        """Reset only the current round (keeps scores)"""
        # This method is here for compatibility but doesn't do much
        # as each round is independent
        pass
    
    def get_scores(self) -> Tuple[int, int, int]:
        """
        Get current game scores
        
        Returns:
            Tuple of (player_score, computer_score, rounds_played)
        """
        return self.player_score, self.computer_score, self.rounds_played
