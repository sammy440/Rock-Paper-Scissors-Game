"""
Bluetooth Client for Rock-Paper-Scissors Multiplayer
Requires PyBluez or Bleak library

Installation:
    pip install pybluez  # For classic Bluetooth (Linux/Windows)
    pip install bleak    # For Bluetooth Low Energy (cross-platform)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import create_message, parse_message

# Try to import Bluetooth libraries
try:
    import bluetooth
    BLUETOOTH_AVAILABLE = True
    BLUETOOTH_TYPE = "classic"
except ImportError:
    try:
        import asyncio
        from bleak import BleakClient, BleakScanner
        BLUETOOTH_AVAILABLE = True
        BLUETOOTH_TYPE = "ble"
    except ImportError:
        BLUETOOTH_AVAILABLE = False
        BLUETOOTH_TYPE = None


class BluetoothClient:
    """Bluetooth client for multiplayer Rock-Paper-Scissors"""
    
    def __init__(self):
        if not BLUETOOTH_AVAILABLE:
            raise ImportError(
                "No Bluetooth library found. Please install:\n"
                "  pip install pybluez  (for classic Bluetooth)\n"
                "  or\n"
                "  pip install bleak    (for Bluetooth Low Energy)"
            )
        
        self.bluetooth_type = BLUETOOTH_TYPE
        self.socket = None
        self.running = False
    
    def find_service(self):
        """Find the Rock-Paper-Scissors service"""
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        
        print("🔍 Searching for Rock-Paper-Scissors game servers...")
        print("This may take a moment...\n")
        
        services = bluetooth.find_service(uuid=uuid)
        
        if not services:
            print("❌ No game servers found!")
            print("Make sure the server is running and Bluetooth is enabled.")
            return None
        
        print(f"✅ Found {len(services)} server(s):\n")
        for i, service in enumerate(services):
            print(f"{i + 1}. {service['name']}")
            print(f"   Host: {service['host']}")
            print(f"   Port: {service['port']}")
            print()
        
        return services
    
    def connect_classic(self, host=None, port=None):
        """Connect using classic Bluetooth (PyBluez)"""
        try:
            # If no host/port provided, search for services
            if not host or not port:
                services = self.find_service()
                if not services:
                    return
                
                # Use first service found
                service = services[0]
                host = service['host']
                port = service['port']
                print(f"Connecting to {service['name']} at {host}:{port}...")
            
            # Create socket and connect
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((host, port))
            
            print("✅ Connected to server!")
            self.running = True
            
            # Receive handshake
            data = self.socket.recv(1024).decode().strip()
            handshake = parse_message(data)
            
            if handshake and handshake.get("type") == "handshake":
                print(f"🤝 Handshake received from {handshake.get('player')}")
                self.game_loop()
            else:
                print("❌ Invalid handshake from server")
                
        except bluetooth.BluetoothError as e:
            print(f"❌ Bluetooth error: {e}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        finally:
            self.disconnect()
    
    def game_loop(self):
        """Main game loop"""
        print("\n🎮 Game started! Type 'Rock', 'Paper', or 'Scissors' to play")
        print("Type 'quit' to exit\n")
        
        round_num = 0
        client_score = 0
        server_score = 0
        
        while self.running:
            try:
                round_num += 1
                print(f"\n--- Round {round_num} ---")
                
                # Wait for server move
                print("⏳ Waiting for opponent to make a move...")
                data = self.socket.recv(1024).decode().strip()
                
                if not data:
                    print("❌ Connection lost!")
                    break
                
                server_msg = parse_message(data)
                
                if server_msg and server_msg.get("type") == "move":
                    print("✅ Opponent has made their move")
                    
                    # Get client move
                    client_move = None
                    while client_move not in ["Rock", "Paper", "Scissors"]:
                        move_input = input("Your move (Rock/Paper/Scissors): ").strip()
                        
                        if move_input.lower() == 'quit':
                            disconnect_msg = create_message("disconnect")
                            self.socket.send(disconnect_msg + "\n")
                            self.running = False
                            break
                        
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
                    self.socket.send(move_msg + "\n")
                    print(f"✅ Sent your move: {client_move}")
                    
                    # Wait for result
                    print("⏳ Waiting for result...")
                    result_data = self.socket.recv(1024).decode().strip()
                    result_msg = parse_message(result_data)
                    
                    if result_msg and result_msg.get("type") == "result":
                        winner = result_msg.get("winner")
                        server_move = result_msg.get("server_move")
                        client_move_result = result_msg.get("client_move")
                        server_score = result_msg.get("server_score", 0)
                        client_score = result_msg.get("client_score", 0)
                        
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
                        print(f"\n📊 Score: {client_score} - {server_score}")
                        print("=" * 40)
                
                elif server_msg and server_msg.get("type") == "disconnect":
                    print("👋 Server disconnected")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Disconnecting...")
                break
            except Exception as e:
                print(f"❌ Error in game loop: {e}")
                break
    
    def disconnect(self):
        """Disconnect from the server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("\n👋 Disconnected from server")
    
    def connect(self, host=None, port=None):
        """Connect to the appropriate Bluetooth server"""
        if self.bluetooth_type == "classic":
            self.connect_classic(host, port)
        elif self.bluetooth_type == "ble":
            print("⚠️ BLE client not fully implemented yet.")
            print("Please use classic Bluetooth (PyBluez) or Wi-Fi multiplayer.")
        else:
            print("❌ No Bluetooth support available")


def main():
    """Main function to start the Bluetooth client"""
    import argparse
    
    if not BLUETOOTH_AVAILABLE:
        print("❌ Bluetooth library not found!")
        print("\nPlease install one of the following:")
        print("  pip install pybluez  # For classic Bluetooth")
        print("  pip install bleak    # For Bluetooth Low Energy")
        return
    
    print(f"Using {BLUETOOTH_TYPE} Bluetooth")
    
    parser = argparse.ArgumentParser(description='Rock-Paper-Scissors Bluetooth Client')
    parser.add_argument('--host', help='Server Bluetooth address (optional, will search if not provided)')
    parser.add_argument('--port', type=int, help='Server port (optional)')
    args = parser.parse_args()
    
    client = BluetoothClient()
    client.connect(args.host, args.port)


if __name__ == "__main__":
    main()
