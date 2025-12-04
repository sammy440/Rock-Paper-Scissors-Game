"""
Wi-Fi Server for Rock-Paper-Scissors Multiplayer
Hosts a game and waits for a client to connect
"""

import socket
import threading
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game_logic import GameLogic
from utils import get_local_ip, create_message, parse_message


class WiFiServer:
    """Wi-Fi server for multiplayer Rock-Paper-Scissors"""
    
    def __init__(self, host='0.0.0.0', port=50007):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.game_logic = GameLogic()
        self.running = False
        
        self.server_move = None
        self.client_move = None
        self.current_round = 0
        
    def start(self):
        """Start the server and listen for connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            self.running = True
            local_ip = get_local_ip()
            
            print("=" * 60)
            print("🎮 Rock-Paper-Scissors Server Started!")
            print("=" * 60)
            print(f"Server IP: {local_ip}")
            print(f"Server Port: {self.port}")
            print(f"\nShare this information with the client:")
            print(f"  IP: {local_ip}")
            print(f"  Port: {self.port}")
            print("=" * 60)
            print("Waiting for client to connect...")
            
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f"\n✅ Client connected from {self.client_address}")
            
            # Send handshake
            handshake = create_message("handshake", player="server", version="1.0")
            self.send_message(handshake)
            
            # Start game loop
            self.game_loop()
            
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.stop()
    
    def send_message(self, message):
        """Send a message to the client"""
        try:
            self.client_socket.sendall((message + "\n").encode())
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def receive_message(self):
        """Receive a message from the client"""
        try:
            data = self.client_socket.recv(1024).decode().strip()
            return parse_message(data)
        except Exception as e:
            print(f"❌ Error receiving message: {e}")
            return None
    
    def game_loop(self):
        """Main game loop"""
        print("\n🎮 Game started! Type 'Rock', 'Paper', or 'Scissors' to play")
        print("Type 'quit' to exit\n")
        
        while self.running:
            try:
                self.current_round += 1
                print(f"\n--- Round {self.current_round} ---")
                
                # Get server move
                self.server_move = None
                while self.server_move not in ["Rock", "Paper", "Scissors"]:
                    move_input = input("Your move (Rock/Paper/Scissors): ").strip()
                    
                    if move_input.lower() == 'quit':
                        disconnect_msg = create_message("disconnect")
                        self.send_message(disconnect_msg)
                        self.running = False
                        break
                    
                    # Capitalize first letter
                    move_input = move_input.capitalize()
                    if move_input in ["Rock", "Paper", "Scissors"]:
                        self.server_move = move_input
                    else:
                        print("❌ Invalid move! Please choose Rock, Paper, or Scissors")
                
                if not self.running:
                    break
                
                # Send move to client
                move_msg = create_message("move", player="server", 
                                         move=self.server_move, round=self.current_round)
                self.send_message(move_msg)
                print(f"✅ Sent your move: {self.server_move}")
                
                # Wait for client move
                print("⏳ Waiting for opponent's move...")
                client_msg = self.receive_message()
                
                if client_msg is None:
                    print("❌ Connection lost!")
                    break
                
                if client_msg.get("type") == "disconnect":
                    print("👋 Client disconnected")
                    break
                
                if client_msg.get("type") == "move":
                    self.client_move = client_msg.get("move")
                    print(f"📨 Received opponent's move: {self.client_move}")
                    
                    # Determine winner
                    result = self.game_logic.decide_winner(self.server_move, self.client_move)
                    
                    if result == "player1":
                        self.game_logic.player_score += 1
                        outcome = "You Win!"
                        winner = "server"
                    elif result == "player2":
                        self.game_logic.computer_score += 1
                        outcome = "You Lose!"
                        winner = "client"
                    else:
                        outcome = "It's a Tie!"
                        winner = "tie"
                    
                    # Send result to client
                    result_msg = create_message("result", 
                                               winner=winner,
                                               server_move=self.server_move,
                                               client_move=self.client_move,
                                               server_score=self.game_logic.player_score,
                                               client_score=self.game_logic.computer_score,
                                               round=self.current_round)
                    self.send_message(result_msg)
                    
                    # Display result
                    print("\n" + "=" * 40)
                    print(f"🎯 {outcome}")
                    print(f"   You: {self.server_move}")
                    print(f"   Opponent: {self.client_move}")
                    print(f"\n📊 Score: {self.game_logic.player_score} - {self.game_logic.computer_score}")
                    print("=" * 40)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Server shutting down...")
                disconnect_msg = create_message("disconnect")
                self.send_message(disconnect_msg)
                break
            except Exception as e:
                print(f"❌ Error in game loop: {e}")
                break
    
    def stop(self):
        """Stop the server and close connections"""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("\n👋 Server stopped")


def main():
    """Main function to start the Wi-Fi server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Rock-Paper-Scissors Wi-Fi Server')
    parser.add_argument('--port', type=int, default=50007, help='Port to listen on')
    args = parser.parse_args()
    
    server = WiFiServer(port=args.port)
    server.start()


if __name__ == "__main__":
    main()
