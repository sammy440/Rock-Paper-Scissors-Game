"""
Wi-Fi Client for Rock-Paper-Scissors Multiplayer
Connects to a server to play multiplayer
"""

import socket
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import create_message, parse_message


class WiFiClient:
    """Wi-Fi client for multiplayer Rock-Paper-Scissors"""
    
    def __init__(self, host, port=50007):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        self.client_score = 0
        self.server_score = 0
        
    def connect(self):
        """Connect to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"🔌 Connecting to {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            print("✅ Connected to server!")
            
            # Receive handshake
            handshake = self.receive_message()
            if handshake and handshake.get("type") == "handshake":
                print(f"🤝 Handshake received from {handshake.get('player')}")
                self.running = True
                
                # Start game loop
                self.game_loop()
            else:
                print("❌ Invalid handshake from server")
                
        except ConnectionRefusedError:
            print("❌ Connection refused. Make sure the server is running.")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        finally:
            self.disconnect()
    
    def send_message(self, message):
        """Send a message to the server"""
        try:
            self.socket.sendall((message + "\n").encode())
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def receive_message(self):
        """Receive a message from the server"""
        try:
            data = self.socket.recv(1024).decode().strip()
            return parse_message(data)
        except Exception as e:
            print(f"❌ Error receiving message: {e}")
            return None
    
    def game_loop(self):
        """Main game loop"""
        print("\n🎮 Game started! Type 'Rock', 'Paper', or 'Scissors' to play")
        print("Type 'quit' to exit\n")
        
        round_num = 0
        
        while self.running:
            try:
                round_num += 1
                print(f"\n--- Round {round_num} ---")
                
                # Wait for server move first
                print("⏳ Waiting for opponent to make a move...")
                server_msg = self.receive_message()
                
                if server_msg is None:
                    print("❌ Connection lost!")
                    break
                
                if server_msg.get("type") == "disconnect":
                    print("👋 Server disconnected")
                    break
                
                if server_msg.get("type") == "move":
                    print("✅ Opponent has made their move")
                    
                    # Get client move
                    client_move = None
                    while client_move not in ["Rock", "Paper", "Scissors"]:
                        move_input = input("Your move (Rock/Paper/Scissors): ").strip()
                        
                        if move_input.lower() == 'quit':
                            disconnect_msg = create_message("disconnect")
                            self.send_message(disconnect_msg)
                            self.running = False
                            break
                        
                        # Capitalize first letter
                        move_input = move_input.capitalize()
                        if move_input in ["Rock", "Paper", "Scissors"]:
                            client_move = move_input
                        else:
                            print("❌ Invalid move! Please choose Rock, Paper, or Scissors")
                    
                    if not self.running:
                        break
                    
                    # Send move to server
                    move_msg = create_message("move", player="client", 
                                             move=client_move, round=round_num)
                    self.send_message(move_msg)
                    print(f"✅ Sent your move: {client_move}")
                    
                    # Wait for result
                    print("⏳ Waiting for result...")
                    result_msg = self.receive_message()
                    
                    if result_msg and result_msg.get("type") == "result":
                        winner = result_msg.get("winner")
                        server_move = result_msg.get("server_move")
                        client_move_result = result_msg.get("client_move")
                        self.server_score = result_msg.get("server_score", 0)
                        self.client_score = result_msg.get("client_score", 0)
                        
                        # Determine outcome
                        if winner == "client":
                            outcome = "You Win!"
                        elif winner == "server":
                            outcome = "You Lose!"
                        else:
                            outcome = "It's a Tie!"
                        
                        # Display result
                        print("\n" + "=" * 40)
                        print(f"🎯 {outcome}")
                        print(f"   You: {client_move_result}")
                        print(f"   Opponent: {server_move}")
                        print(f"\n📊 Score: {self.client_score} - {self.server_score}")
                        print("=" * 40)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Disconnecting...")
                disconnect_msg = create_message("disconnect")
                self.send_message(disconnect_msg)
                break
            except Exception as e:
                print(f"❌ Error in game loop: {e}")
                break
    
    def disconnect(self):
        """Disconnect from the server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("\n👋 Disconnected from server")


def main():
    """Main function to start the Wi-Fi client"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Rock-Paper-Scissors Wi-Fi Client')
    parser.add_argument('host', help='Server IP address')
    parser.add_argument('--port', type=int, default=50007, help='Server port')
    args = parser.parse_args()
    
    client = WiFiClient(args.host, args.port)
    client.connect()


if __name__ == "__main__":
    main()
