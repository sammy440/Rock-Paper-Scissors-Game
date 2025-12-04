# 🎮 Rock-Paper-Scissors Game

A modern desktop Rock-Paper-Scissors game built with **Python** and **Tkinter**, featuring both single-player and multiplayer modes.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 🎨 **Dark/Light Mode**
- Toggle between beautiful dark and light themes
- Smooth theme transitions
- Persistent across all screens
- Easy-to-use moon/sun toggle button

### 🎯 **Single Player Mode**
- Clean, modern UI with custom-designed buttons
- Play against an AI opponent with random move generation
- Real-time score tracking
- Round-by-round history
- Smooth hover effects and visual feedback
- Color-coded results (Green=Win, Red=Lose, Yellow=Tie)

### 🌐 **Multiplayer Mode (Wi-Fi) - Fully Integrated**
- **Host games** directly from the GUI with one click
- **Join games** with easy IP input interface
- Real-time move synchronization
- Live connection status updates
- Integrated chat-like game interface
- Automatic server/client setup
- Graceful disconnect handling
- No need for separate terminal windows!

### 📱 **Multiplayer Mode (Bluetooth)**
- Connect via Bluetooth using PyBluez
- Service discovery for automatic server detection
- Classic Bluetooth (RFCOMM) support
- Requires PyBluez library installation
- Command-line interface for Bluetooth games

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or newer
- Tkinter (usually bundled with Python)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd "Rock-Paper-Scissors Game"
   ```

3. **Run the game**
   ```bash
   python src/main.py
   ```

## 🎮 How to Play

### 🎨 **Theme Toggle**
- Click the **🌙 moon** icon (light mode) or **☀️ sun** icon (dark mode) in the top-right corner
- Instantly switch between beautiful dark and light themes
- Theme persists across all screens
- Try both - they're both stunning!

### 🎯 **Single Player Mode**
1. Launch the game and click **"🎮 Single Player vs AI"**
2. Choose your move: Rock 🪨, Paper 📄, or Scissors ✂️
3. See instant results with color-coded feedback:
   - 🟢 **Green** = You Win!
   - 🔴 **Red** = You Lose
   - 🟡 **Yellow** = Tie
4. Track your score and rounds played
5. Click **"Reset Scores"** to start fresh
6. Click **"Back to Menu"** to return

### 🌐 **Wi-Fi Multiplayer - Fully Integrated GUI!**

**Everything happens in the app - no terminal needed!** 🎉

#### **Hosting a Game:**
1. Click **"📡 Multiplayer (Wi-Fi)"**
2. Click **"🏠 Host Game"**
3. Your **IP address** and **port** will be displayed
4. **Share this information** with your friend (via text, Discord, etc.)
5. Wait for connection (you'll see a status update)
6. Once connected, play directly in the GUI!
7. Choose your moves and see results in real-time

#### **Joining a Game:**
1. Click **"📡 Multiplayer (Wi-Fi)"**
2. Click **"🔗 Join Game"**
3. Enter the **host's IP address** (they'll give you this)
4. Enter the **port** (default: 50007)
5. Click **"Connect"**
6. Wait for connection confirmation
7. Start playing!

#### **During Multiplayer:**
- Choose Rock, Paper, or Scissors
- Wait for your opponent's move
- Results appear automatically
- Scores are tracked for both players
- Click **"Disconnect"** to end the game

### 📱 **Bluetooth Multiplayer (Advanced)**

**Note:** Bluetooth requires PyBluez library and command-line usage.

#### **Installation:**
```bash
pip install pybluez
```

#### **Host a Bluetooth Game:**
1. Open a terminal
2. Run:
   ```bash
   python multiplayer/bluetooth_server.py
   ```
3. Share your Bluetooth address with your friend
4. Wait for connection
5. Play via terminal commands

#### **Join a Bluetooth Game:**
1. Open a terminal
2. Run (auto-discovery):
   ```bash
   python multiplayer/bluetooth_client.py
   ```
   Or specify host:
   ```bash
   python multiplayer/bluetooth_client.py --host XX:XX:XX:XX:XX:XX
   ```
3. Follow the prompts to play

---

## 🎨 UI Features

### **Light Mode** ☀️
- Clean white background (#FFFFFF)
- Vibrant accent colors:
  - 🔵 Blue (#1A73E8) - Primary actions
  - 🟢 Green (#34A853) - Success/Multiplayer
  - 🟡 Yellow (#FBBC04) - Warnings/Bluetooth
  - 🔴 Red (#EA4335) - Danger/Exit
- Professional, modern aesthetic
- Perfect for daytime use

### **Dark Mode** 🌙
- Rich dark background (#1E1E1E)
- Eye-friendly colors:
  - 🔵 Soft Blue (#4A9EFF)
  - 🟢 Gentle Green (#5CB85C)
  - 🟡 Warm Yellow (#F0AD4E)
  - 🔴 Muted Red (#D9534F)
- Reduces eye strain
- Perfect for night gaming
- Absolutely gorgeous! ✨

### **Design Elements**
- **Custom Rounded Buttons**: Smooth hover effects
- **Emoji Icons**: Visual and fun (🪨📄✂️)
- **Color-Coded Results**: Instant visual feedback
- **Responsive Layout**: Optimized 550x700 window
- **Modern Typography**: Helvetica font family
- **Smooth Transitions**: Polished user experience

## 🧪 Running Tests

Run the unit tests to verify game logic:

```bash
python tests/test_game_logic.py
```

## 📁 Project Structure

```
rock-paper-scissors/
├── src/
│   ├── main.py           # Main entry point
│   ├── ui.py             # User interface
│   ├── game_logic.py     # Game rules and logic
│   └── utils.py          # Utility functions
├── multiplayer/
│   ├── wifi_server.py    # Wi-Fi server
│   └── wifi_client.py    # Wi-Fi client
├── tests/
│   └── test_game_logic.py # Unit tests
├── requirements (2).md    # Detailed requirements
└── README.md             # This file
```

## 🎨 UI Features

- **Modern Design**: Clean, minimal interface with professional styling
- **Custom Buttons**: Rounded buttons with smooth hover effects
- **Color Coded Results**: 
  - 🟢 Green for wins
  - 🔴 Red for losses
  - 🟡 Yellow for ties
- **Responsive Layout**: Fixed window size optimized for gameplay
- **Emoji Support**: Visual icons for Rock 🪨, Paper 📄, and Scissors ✂️

## 🔧 Technical Details

### Game Rules
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- Same choice = Tie

### Network Protocol
The multiplayer mode uses JSON messages over TCP:

```json
{
  "type": "move",
  "player": "player1",
  "move": "Rock",
  "round": 2
}
```

Message types:
- `handshake` - Initial connection
- `move` - Player's move
- `result` - Round outcome
- `disconnect` - Graceful disconnect

## 🛠️ Customization

### Changing Server Port
```bash
python multiplayer/wifi_server.py --port 12345
python multiplayer/wifi_client.py <HOST_IP> --port 12345
```

## 🐛 Troubleshooting

### Wi-Fi Connection Issues
- Ensure both devices are on the same network
- Check firewall settings
- Verify the correct IP address is being used

### UI Not Displaying Correctly
- Ensure Tkinter is properly installed
- Try updating Python to the latest version

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Built as a portfolio project demonstrating:
- Python GUI development with Tkinter
- Network programming with sockets
- Game logic implementation
- Clean code architecture
- Unit testing

## 🔮 Future Enhancements

- [ ] Dark mode theme toggle
- [ ] Sound effects
- [ ] Animations for moves
- [ ] AI difficulty levels
- [ ] Local leaderboard
- [ ] Best-of-N game modes
- [ ] Bluetooth multiplayer implementation
- [ ] Online matchmaking

---

**Enjoy the game! 🎮**
