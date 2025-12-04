"""
Utility functions for the Rock-Paper-Scissors game
"""

import socket
import json
from typing import Optional


def get_local_ip() -> str:
    """
    Get the local IP address of the machine
    
    Returns:
        Local IP address as string
    """
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a public DNS (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def validate_move(move: str) -> bool:
    """
    Validate if a move is valid
    
    Args:
        move: The move to validate
        
    Returns:
        True if valid, False otherwise
    """
    return move in ["Rock", "Paper", "Scissors"]


def create_message(msg_type: str, **kwargs) -> str:
    """
    Create a JSON message for network communication
    
    Args:
        msg_type: Type of message (handshake, move, result, ping, pong, disconnect)
        **kwargs: Additional data to include in the message
        
    Returns:
        JSON string
    """
    message = {"type": msg_type, **kwargs}
    return json.dumps(message)


def parse_message(data: str) -> Optional[dict]:
    """
    Parse a JSON message
    
    Args:
        data: JSON string to parse
        
    Returns:
        Parsed dictionary or None if invalid
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


def format_score(player_score: int, opponent_score: int) -> str:
    """
    Format score for display
    
    Args:
        player_score: Player's score
        opponent_score: Opponent's score
        
    Returns:
        Formatted score string
    """
    return f"{player_score} - {opponent_score}"
