# requirements.md
## Rock–Paper–Scissors Game (Python + Tkinter)

### Project Overview
The **Rock–Paper–Scissors Game** is a modern desktop application built with **Python** and **Tkinter**.
It features a clean, minimal user interface, smooth interactions, and multiple play modes including:

- **Single Player vs Computer (AI)**
- **Local Multiplayer via Bluetooth or Wi‑Fi Hotspot (P2P communication)**

This project is designed for beginner–intermediate Python developers looking to build a visually appealing GUI application while learning event handling, game logic, and peer‑to‑peer networking.

---

## Core Features

### 1. Single-Player Mode
- Clean & modern UI (flat design, custom fonts, spacing)
- Button-based selection: Rock, Paper, Scissors
- Random AI decision-making
- Win/Loss/Tie detection engine
- Real-time result display
- Scoreboard (Player vs Computer)
- Reset round / Reset scoreboard

### 2. Multiplayer Mode (Optional)
Provide two multiplayer options: Bluetooth or Wi‑Fi Hotspot (local P2P).

#### A. Bluetooth Multiplayer
- Use `PyBluez` (classic Bluetooth) or `Bleak` (BLE) depending on platform support.
- Host/server mode and client mode:
  - Host advertises a service and listens for a connection.
  - Client scans and connects to the host.
- Exchange small JSON-like move packets (e.g., `{"player_move":"Rock","round":3}`).
- Server validates moves and broadcasts results to both players.
- Handle pairing, connection lost, and reconnection flow.
- Requirements:
  - Bluetooth adapter on both devices.
  - Proper platform-specific dependencies (PyBluez tends to work better on Linux; Bleak for cross-platform BLE).

#### B. Hotspot / Wi-Fi Multiplayer
- Use Python's `socket` module (TCP) to create a simple server-client model.
- Host opens a TCP server on a chosen port and displays its local IP and port for the client to connect.
- Client connects using host IP + port.
- Exchange JSON strings for moves and game state synchronization.
- Requirements:
  - Both devices on the same Wi‑Fi network or one device acting as a mobile hotspot.
  - Firewall rules/permissions allowing local TCP connections.

---

## UI/UX Requirements
- Clean, minimal layout using Tkinter frames and `ttk` widgets.
- Consistent margins/padding and readable typography.
- Custom font styles (e.g., 'Helvetica' or a bundled TTF).
- Smooth vertical spacing between elements and balanced whitespace.
- Light color palette by default (e.g., white background `#FFFFFF`, soft gray `#F7F7F7`, blue accent `#1A73E8`).
- Optional PNG/SVG icons for Rock/Paper/Scissors.
- Responsive minimum window size (suggested 400×450).
- Accessibility: readable font-size (≥12pt), keyboard navigation, clear contrast.
- Animations: subtle hover effects on buttons (using custom bindings) and transition feedback for results.
- Sound/SFX (optional): short sound on win/lose/tie with ability to mute.

---

## Technical Requirements

### Software
- Python 3.8 or newer
- Tkinter (bundled with most Python installations)
- For packaging: PyInstaller (for Windows `.exe`) or `py2app`/`pyinstaller` on macOS/Linux
- For Bluetooth multiplayer:
  - `PyBluez` or `Bleak`
- For Wi‑Fi multiplayer:
  - no extra dependencies; use Python's `socket`
- Recommended: `python-dotenv` for local config of host/port during development

### Hardware
- Desktop or laptop with Bluetooth adapter for Bluetooth mode (if used)
- Network access (Wi‑Fi/hotspot) for Wi‑Fi multiplayer

---

## Project Structure (Suggested)
```
rock-paper-scissors/
│── assets/
│     ├── icons/
│     │   ├── rock.png
│     │   ├── paper.png
│     │   └── scissors.png
│     └── fonts/
│         └── CustomFont.ttf
│
│── multiplayer/
│     ├── bluetooth_server.py
│     ├── bluetooth_client.py
│     ├── wifi_server.py
│     └── wifi_client.py
│
│── src/
│     ├── main.py
│     ├── ui.py
│     ├── game_logic.py
│     └── utils.py
│
│── tests/
│     ├── test_game_logic.py
│     └── test_networking.py
│
│── requirements.md
│── README.md
│── LICENSE
```

---

## Game Logic Requirements
- Moves: Rock, Paper, Scissors
- Rules:
  - Rock beats Scissors
  - Scissors beats Paper
  - Paper beats Rock
  - Same choice → Tie
- Best-of options (e.g., best-of-3, best-of-5) as a configurable setting
- Round number tracking and per-round history (optional)
- Deterministic tie-breaker behavior if implementing timed moves

---

## Networking Protocol (Suggested)
Use simple JSON over TCP/Bluetooth socket.

### Packet Example (JSON string)
```json
{
  "type": "move",
  "player": "player1",
  "move": "Rock",
  "round": 2
}
```

### Message Types
- `handshake` - initial connection info (player name, version)
- `move` - the player's move for the round
- `result` - round outcome and updated scores
- `ping` / `pong` - keepalive
- `disconnect` - graceful disconnect notice

---

## Error Handling & Edge Cases
- Handle disconnects and network timeouts with retries and user feedback.
- Validate packet contents and ignore malformed packets.
- Prevent duplicate move submissions per round.
- Gracefully handle unexpected exceptions and show user-friendly error messages.
- Allow returning to main menu on errors (option to retry or quit match).

---

## Testing Requirements
- Unit tests for game logic (all win/tie/lose permutations).
- Integration tests for server-client exchange (simulate socket messages).
- Manual tests:
  - UI loads and behaves in single-player mode.
  - AI randomness fairness across many rounds.
  - Bluetooth pairing/connect/disconnect flows.
  - Wi‑Fi hotspot local network connection stability.
  - Score sync and desync recovery.
- Cross-platform checks for Bluetooth libraries (Windows/macOS/Linux differences).

---

## Packaging & Distribution
### Windows .exe (optional)
- Use PyInstaller:
```
pyinstaller --onefile --windowed src/main.py
```
- Include assets folder using `--add-data` flags.

### macOS
- `py2app` or PyInstaller (check compatibility).

### Linux
- Distribute as a packaged executable or provide installation script (venv + pip install -r requirements.txt).

---

## Security & Privacy
- Do not send any sensitive personal information over the local connection.
- Use minimal data in packets: moves and player name only.
- Consider adding a simple handshake token or PIN for private matches.

---

## Future Enhancements
- Dark mode theme toggle.
- Leaderboard stored locally (JSON) or remotely (optional).
- Sound effects and animations.
- Online matchmaking via a lightweight server (WebSockets).
- Spectator mode (third device observes a match).
- AI difficulty levels with simple heuristics or Markov-chain based prediction.

---

## Development Timeline (suggested)
- Day 1–2: Design UI & implement single-player game loop.
- Day 3: Add scoreboard, animations, and icons.
- Day 4–5: Implement Wi‑Fi multiplayer (server/client) and local testing.
- Day 6–7: Implement Bluetooth multiplayer, handle platform differences.
- Day 8: Testing, packaging, and documentation.

---

## Appendix: Useful Code Snippets

### Simple game logic (game_logic.py)
```python
def decide_winner(p1_move, p2_move):
    if p1_move == p2_move:
        return "tie"
    wins = {
        "Rock": "Scissors",
        "Scissors": "Paper",
        "Paper": "Rock"
    }
    if wins[p1_move] == p2_move:
        return "player1"
    return "player2"
```

### Simple TCP server snippet (wifi_server.py)
```python
import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 50007

def client_thread(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = json.loads(data.decode())
            # handle message

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening on", PORT)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()
```

---

Thank you for the note — this file now contains the full, detailed project requirements including Bluetooth and hotspot multiplayer details.
