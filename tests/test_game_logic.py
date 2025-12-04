"""
Unit tests for game logic
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game_logic import GameLogic


class TestGameLogic(unittest.TestCase):
    """Test cases for GameLogic class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = GameLogic()
    
    def test_rock_beats_scissors(self):
        """Test that Rock beats Scissors"""
        result = self.game.decide_winner("Rock", "Scissors")
        self.assertEqual(result, "player1")
    
    def test_scissors_beats_paper(self):
        """Test that Scissors beats Paper"""
        result = self.game.decide_winner("Scissors", "Paper")
        self.assertEqual(result, "player1")
    
    def test_paper_beats_rock(self):
        """Test that Paper beats Rock"""
        result = self.game.decide_winner("Paper", "Rock")
        self.assertEqual(result, "player1")
    
    def test_rock_loses_to_paper(self):
        """Test that Rock loses to Paper"""
        result = self.game.decide_winner("Rock", "Paper")
        self.assertEqual(result, "player2")
    
    def test_scissors_loses_to_rock(self):
        """Test that Scissors loses to Rock"""
        result = self.game.decide_winner("Scissors", "Rock")
        self.assertEqual(result, "player2")
    
    def test_paper_loses_to_scissors(self):
        """Test that Paper loses to Scissors"""
        result = self.game.decide_winner("Paper", "Scissors")
        self.assertEqual(result, "player2")
    
    def test_rock_ties_rock(self):
        """Test that Rock ties with Rock"""
        result = self.game.decide_winner("Rock", "Rock")
        self.assertEqual(result, "tie")
    
    def test_paper_ties_paper(self):
        """Test that Paper ties with Paper"""
        result = self.game.decide_winner("Paper", "Paper")
        self.assertEqual(result, "tie")
    
    def test_scissors_ties_scissors(self):
        """Test that Scissors ties with Scissors"""
        result = self.game.decide_winner("Scissors", "Scissors")
        self.assertEqual(result, "tie")
    
    def test_score_tracking(self):
        """Test that scores are tracked correctly"""
        self.game.play_round("Rock", "Scissors")  # Player wins
        self.assertEqual(self.game.player_score, 1)
        self.assertEqual(self.game.computer_score, 0)
        
        self.game.play_round("Rock", "Paper")  # Player loses
        self.assertEqual(self.game.player_score, 1)
        self.assertEqual(self.game.computer_score, 1)
        
        self.game.play_round("Rock", "Rock")  # Tie
        self.assertEqual(self.game.player_score, 1)
        self.assertEqual(self.game.computer_score, 1)
    
    def test_rounds_played(self):
        """Test that rounds are counted correctly"""
        self.game.play_round("Rock", "Scissors")
        self.game.play_round("Paper", "Rock")
        self.game.play_round("Scissors", "Paper")
        
        self.assertEqual(self.game.rounds_played, 3)
    
    def test_reset_scores(self):
        """Test that reset_scores works correctly"""
        self.game.play_round("Rock", "Scissors")
        self.game.play_round("Paper", "Rock")
        
        self.game.reset_scores()
        
        self.assertEqual(self.game.player_score, 0)
        self.assertEqual(self.game.computer_score, 0)
        self.assertEqual(self.game.rounds_played, 0)
        self.assertEqual(len(self.game.history), 0)
    
    def test_computer_move_validity(self):
        """Test that computer generates valid moves"""
        for _ in range(100):
            move = self.game.get_computer_move()
            self.assertIn(move, ["Rock", "Paper", "Scissors"])
    
    def test_history_tracking(self):
        """Test that game history is tracked"""
        self.game.play_round("Rock", "Scissors")
        self.game.play_round("Paper", "Rock")
        
        self.assertEqual(len(self.game.history), 2)
        self.assertEqual(self.game.history[0]["player_move"], "Rock")
        self.assertEqual(self.game.history[0]["computer_move"], "Scissors")
        self.assertEqual(self.game.history[1]["player_move"], "Paper")
        self.assertEqual(self.game.history[1]["computer_move"], "Rock")


if __name__ == '__main__':
    unittest.main()
