# 🚀 Quick Start Guide - Updated!

## 🎮 Running the Game

### **Easiest Way: Just Launch It!**

1. **Open a terminal/command prompt**
2. **Navigate to the game directory:**
   ```bash
   cd "c:\Users\USER\Desktop\Rock-Paper-Scissors Game"
   ```
3. **Run the game:**
   ```bash
   python src/main.py
   ```
4. **That's it!** The beautiful GUI will appear with all features ready to use.

---

## 🎨 New Features!

### **Dark/Light Mode Toggle**
- Look for the **🌙 moon** or **☀️ sun** icon in the top-right corner
- Click it to switch between dark and light themes
- Works on all screens!
- Try it out - it looks amazing! ✨

---

## 🎯 Single Player Mode

1. Click **"🎮 Single Player vs AI"**
2. Choose Rock 🪨, Paper 📄, or Scissors ✂️
3. Watch the results appear instantly
4. Track your score in real-time
5. Click **"Reset Scores"** to start fresh
6. **Toggle theme** anytime with the moon/sun button!

---

## 🌐 Wi-Fi Multiplayer (Now Fully Integrated!)

### **No More Terminal Windows!** Everything is in the GUI now! 🎉

### **Option 1: Host a Game**

1. Click **"📡 Multiplayer (Wi-Fi)"**
2. Click **"🏠 Host Game"**
3. The app will show your **IP address** and **port**
4. **Share this info** with your friend (via text, Discord, etc.)
5. Wait for them to connect
6. Once connected, play directly in the GUI!

### **Option 2: Join a Game**

1. Click **"📡 Multiplayer (Wi-Fi)"**
2. Click **"🔗 Join Game"**
3. Enter your friend's **IP address** (they'll give you this)
4. Enter the **port** (default is 50007)
5. Click **"Connect"**
6. Once connected, start playing!

### **Playing Multiplayer**
- Choose your move (Rock/Paper/Scissors)
- Wait for your opponent
- See the results in real-time
- Scores are tracked automatically
- Click **"Disconnect"** when done

---

## 📱 Bluetooth Multiplayer (Advanced)

### **Requirements:**
- Bluetooth adapter on both devices
- PyBluez library installed: `pip install pybluez`
- Devices should be paired

### **How to Use:**

#### **Host (Server):**
```bash
python multiplayer/bluetooth_server.py
```

#### **Join (Client):**
```bash
python multiplayer/bluetooth_client.py
```
The client will automatically search for available servers!

**Or specify a server manually:**
```bash
python multiplayer/bluetooth_client.py --host XX:XX:XX:XX:XX:XX --port 1
```

---

## 💡 Tips & Tricks

### **Theme Switching**
- 🌙 **Dark Mode**: Perfect for night gaming
- ☀️ **Light Mode**: Great for daytime
- Switch anytime without losing your game!

### **Wi-Fi Multiplayer Tips**
1. **Both players must be on the same network** (or one creates a hotspot)
2. **Find your IP**: The host screen shows it automatically!
3. **Firewall**: Windows may ask to allow Python - click "Allow"
4. **Can't connect?** Double-check the IP address and make sure both are on the same Wi-Fi

### **Best Practices**
- Use **Wi-Fi multiplayer** for the easiest experience
- Try **dark mode** - it looks incredible!
- **Single player** is great for practice
- **Bluetooth** works but requires more setup

---

## 🎨 UI Highlights

### **Light Mode**
- Clean white background
- Vibrant blue, green, red, and yellow buttons
- Professional and modern look

### **Dark Mode**
- Sleek dark background (#1E1E1E)
- Softer, eye-friendly colors
- Perfect for extended gaming sessions
- Looks absolutely stunning! 🌟

---

## 🐛 Troubleshooting

### **"ModuleNotFoundError"**
- Make sure you're in the correct directory
- Verify Python 3.8+ is installed: `python --version`

### **Wi-Fi Connection Issues**
- Both computers must be on the **same network**
- Check **firewall settings** (allow Python)
- Verify the **IP address** is correct
- Make sure the **host is running first**

### **Theme Not Changing**
- The theme should change instantly
- If not, try clicking the toggle again
- Restart the app if needed

### **Bluetooth Issues**
- Install PyBluez: `pip install pybluez`
- Make sure Bluetooth is enabled
- Devices should be paired beforehand
- Use Wi-Fi if Bluetooth doesn't work

---

## 🎯 Quick Command Reference

```bash
# Run the main game (GUI with everything)
python src/main.py

# Run unit tests
python tests/test_game_logic.py

# Bluetooth server (advanced)
python multiplayer/bluetooth_server.py

# Bluetooth client (advanced)
python multiplayer/bluetooth_client.py
```

---

## 🌟 What's New in This Version

✅ **Dark/Light mode toggle** - Beautiful themes!  
✅ **Integrated Wi-Fi multiplayer** - No more terminal windows!  
✅ **Improved UI** - Smoother, more polished  
✅ **Better connection status** - Know exactly what's happening  
✅ **Bluetooth support** - Full implementation with PyBluez  
✅ **Enhanced visuals** - Emojis, better colors, modern design  

---

## 🎮 Ready to Play?

Just run:
```bash
python src/main.py
```

**Enjoy the game! Have fun! �**
