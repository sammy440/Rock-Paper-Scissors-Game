"""
Bluetooth Server for Rock-Paper-Scissors Multiplayer
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
        from bleak import BleakServer, BleakScanner
        BLUETOOTH_AVAILABLE = True
        BLUETOOTH_TYPE = "ble"
    except ImportError:
        BLUETOOTH_AVAILABLE = False
        BLUETOOTH_TYPE = None


class BluetoothServer:
    """Bluetooth server for multiplayer Rock-Paper-Scissors"""
    
    def __init__(self):
        if not BLUETOOTH_AVAILABLE:
            raise ImportError(
                "No Bluetooth library found. Please install:\n"
                "  pip install pybluez  (for classic Bluetooth)\n"
                "  or\n"
                "  pip install bleak    (for Bluetooth Low Energy)"
            )
        
        self.bluetooth_type = BLUETOOTH_TYPE
        self.server_socket = None
        self.client_socket = None
        self.running = False
    
    def start_classic(self):
        """Start classic Bluetooth server using PyBluez"""
        try:
            # Create Bluetooth socket
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            
            # Bind to any available port
            port = bluetooth.PORT_ANY
            self.server_socket.bind(("", port))
            self.server_socket.listen(1)
            
            # Get server info
            host_addr = bluetooth.read_local_bdaddr()[0]
            
            # Advertise service
            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            bluetooth.advertise_service(
                self.server_socket,
                "RockPaperScissors",
                service_id=uuid,
                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
            
            print("=" * 60)
            print("🎮 Rock-Paper-Scissors Bluetooth Server Started!")
            print("=" * 60)
            print(f"Server Address: {host_addr}")
            print(f"Server Port: {port}")
            print(f"Service UUID: {uuid}")
            print("=" * 60)
            print("Waiting for client to connect...")
            print("Make sure Bluetooth is enabled and visible!")
            
            self.running = True
            
            # Accept connection
            self.client_socket, client_info = self.server_socket.accept()
            print(f"\n✅ Client connected: {client_info}")
            
            # Send handshake
            handshake = create_message("handshake", player="server", version="1.0")
            self.client_socket.send(handshake + "\n")
            
            # Game loop
            self.game_loop()
            
        except Exception as e:
            print(f"❌ Bluetooth server error: {e}")
        finally:
            self.stop()
    
    def game_loop(self):
        """Main game loop for Bluetooth"""
        print("\n🎮 Game started! Type 'Rock', 'Paper', or 'Scissors' to play")
        print("Type 'quit' to exit\n")
        
        round_num = 0
        server_score = 0
        client_score = 0
        
        while self.running:
            try:
                round_num += 1
                print(f"\n--- Round {round_num} ---")
                
                # Get server move
                server_move = None
                while server_move not in ["Rock", "Paper", "Scissors"]:
                    move_input = input("Your move (Rock/Paper/Scissors): ").strip()
                    
                    if move_input.lower() == 'quit':
                        disconnect_msg = create_message("disconnect")
                        self.client_socket.send(disconnect_msg + "\n")
                        self.running = False
                        break
                    
                    move_input = move_input.capitalize()
                    if move_input in ["Rock", "Paper", "Scissors"]:
                        server_move = move_input
                    else:
                        print("❌ Invalid move! Please choose Rock, Paper, or Scissors")
                
                if not self.running:
                    break
                
                # Send move to client
                move_msg = create_message("move", player="server", 
                                         move=server_move, round=round_num)
                self.client_socket.send(move_msg + "\n")
                print(f"✅ Sent your move: {server_move}")
                
                # Wait for client move
                print("⏳ Waiting for opponent's move...")
                data = self.client_socket.recv(1024).decode().strip()
                
                if not data:
                    print("❌ Connection lost!")
                    break
                
                client_msg = parse_message(data)
                
                if client_msg and client_msg.get("type") == "move":
                    client_move = client_msg.get("move")
                    print(f"📨 Received opponent's move: {client_move}")
                    
                    # Determine winner
                    from game_logic import GameLogic
                    game = GameLogic()
                    result = game.decide_winner(server_move, client_move)
                    
                    if result == "player1":
                        server_score += 1
                        outcome = "You Win!"
                        winner = "server"
                    elif result == "player2":
                        client_score += 1
                        outcome = "You Lose!"
                        winner = "client"
                    else:
                        outcome = "It's a Tie!"
                        winner = "tie"
                    
                    # Send result
                    result_msg = create_message("result", 
                                               winner=winner,
                                               server_move=server_move,
                                               client_move=client_move,
                                               server_score=server_score,
                                               client_score=client_score,
                                               round=round_num)
                    self.client_socket.send(result_msg + "\n")
                    
                    # Display result
                    print("\n" + "=" * 40)
                    print(f"🎯 {outcome}")
                    print(f"   You: {server_move}")
                    print(f"   Opponent: {client_move}")
                    print(f"\n📊 Score: {server_score} - {client_score}")
                    print("=" * 40)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Server shutting down...")
                break
            except Exception as e:
                print(f"❌ Error in game loop: {e}")
                break
    
    def stop(self):
        """Stop the Bluetooth server"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("\n👋 Bluetooth server stopped")
    
    def start(self):
        """Start the appropriate Bluetooth server"""
        if self.bluetooth_type == "classic":
            self.start_classic()
        elif self.bluetooth_type == "ble":
            print("⚠️ BLE server not fully implemented yet.")
            print("Please use classic Bluetooth (PyBluez) or Wi-Fi multiplayer.")
        else:
            print("❌ No Bluetooth support available")


def main():
    """Main function to start the Bluetooth server"""
    if not BLUETOOTH_AVAILABLE:
        print("❌ Bluetooth library not found!")
        print("\nPlease install one of the following:")
        print("  pip install pybluez  # For classic Bluetooth")
        print("  pip install bleak    # For Bluetooth Low Energy")
        return
    
    print(f"Using {BLUETOOTH_TYPE} Bluetooth")
    
    server = BluetoothServer()
    server.start()


if __name__ == "__main__":
    main()
