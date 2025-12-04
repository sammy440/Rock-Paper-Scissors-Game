# 📦 Creating Executable with PyInstaller

## Complete Guide to Package Your Game for Distribution

This guide will help you create a standalone `.exe` file that users can download and run **without installing Python**!

---

## 🚀 **Quick Start**

### **Step 1: Install PyInstaller**

```bash
pip install pyinstaller
```

### **Step 2: Create the Executable**

Navigate to your project directory and run:

```bash
cd "c:\Users\USER\Desktop\Rock-Paper-Scissors Game"
pyinstaller --onefile --windowed --name "RockPaperScissors" --icon=icon.ico src/main.py
```

**Note:** If you don't have an icon file, remove `--icon=icon.ico` from the command.

### **Step 3: Find Your Executable**

After PyInstaller finishes, you'll find:
- **Executable**: `dist/RockPaperScissors.exe`
- This is the file users can download and run!

---

## 📋 **Detailed Instructions**

### **Method 1: Simple One-File Executable (Recommended)**

This creates a single `.exe` file that's easy to distribute:

```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" src/main.py
```

**Options explained:**
- `--onefile`: Creates a single executable file
- `--windowed`: No console window (GUI only)
- `--name "RockPaperScissors"`: Name of the executable
- `src/main.py`: Your main Python file

**Result:**
- File: `dist/RockPaperScissors.exe`
- Size: ~10-15 MB
- Users just double-click to run!

---

### **Method 2: With Custom Icon (Better Looking)**

First, you need an icon file (`.ico` format).

#### **Option A: Create an Icon**

1. Use an online converter: https://convertio.co/png-ico/
2. Upload a game image (Rock/Paper/Scissors themed)
3. Download the `.ico` file
4. Save it as `icon.ico` in your project root

#### **Option B: Use a Free Icon**

Download a free icon from:
- https://www.flaticon.com/
- https://icons8.com/

Then run:

```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" --icon=icon.ico src/main.py
```

---

### **Method 3: Advanced Build (Smaller Size)**

Create a file called `build.spec` with optimizations:

```bash
# First, generate the spec file
pyinstaller --onefile --windowed --name "RockPaperScissors" src/main.py

# Then edit RockPaperScissors.spec and rebuild
pyinstaller RockPaperScissors.spec
```

---

## 🎯 **Complete Build Script**

I'll create a build script for you to make this easier!

Save this as `build.bat` in your project root:

```batch
@echo off
echo ========================================
echo Building Rock-Paper-Scissors Game
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "RockPaperScissors" --clean src/main.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located at:
echo dist\RockPaperScissors.exe
echo.
echo File size:
dir dist\RockPaperScissors.exe | find "RockPaperScissors.exe"
echo.
pause
```

Then just double-click `build.bat` to build!

---

## 📤 **Distributing to Users**

### **Option 1: GitHub Releases (Recommended)**

1. **Build your executable** (using steps above)

2. **Create a Release on GitHub:**
   - Go to: https://github.com/sammy440/Rock-Paper-Scissors-Game/releases
   - Click "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `Rock-Paper-Scissors Game v1.0.0`
   - Description:
     ```markdown
     # 🎮 Rock-Paper-Scissors Game v1.0.0
     
     ## Features
     - 🎨 Dark/Light mode toggle
     - 🎯 Single player vs AI
     - 🌐 Wi-Fi multiplayer
     - 📱 Bluetooth support (optional)
     
     ## Download
     Download `RockPaperScissors.exe` below and run it!
     No installation required - just double-click to play!
     
     ## System Requirements
     - Windows 10 or later
     - No Python installation needed
     
     ## How to Run
     1. Download `RockPaperScissors.exe`
     2. Double-click to run
     3. Enjoy!
     
     ## For Multiplayer
     - Both players need to be on the same network
     - Windows Firewall may ask for permission - click "Allow"
     ```

3. **Upload the executable:**
   - Drag and drop `dist/RockPaperScissors.exe` into the release
   - Click "Publish release"

4. **Share the link!**
   - Users can download from: `https://github.com/sammy440/Rock-Paper-Scissors-Game/releases`

---

### **Option 2: Direct Download Link**

Upload `RockPaperScissors.exe` to:
- **Google Drive**: Share with "Anyone with the link"
- **Dropbox**: Create a public link
- **OneDrive**: Share link
- **MediaFire**: Free file hosting

Then share the download link!

---

### **Option 3: Installer (Advanced)**

Create a proper installer using **Inno Setup**:

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create an installer script
3. Build an installer that users can run

This is more professional but takes more setup.

---

## 🔧 **Troubleshooting**

### **"PyInstaller not found"**
```bash
pip install pyinstaller
```

### **Executable is too large**
- Normal size: 10-15 MB
- This includes Python runtime
- Can't make it much smaller for GUI apps

### **Antivirus flags the .exe**
- This is normal for PyInstaller executables
- Add an exception in antivirus
- Or sign the executable (advanced, requires certificate)

### **"Failed to execute script"**
- Make sure you used `--windowed` flag
- Check that all imports are correct
- Test the Python script first: `python src/main.py`

### **Missing modules**
If PyInstaller misses some modules, create a `hook` file or use:
```bash
pyinstaller --onefile --windowed --hidden-import=tkinter --name "RockPaperScissors" src/main.py
```

---

## 📊 **Build Comparison**

| Method | File Size | Pros | Cons |
|--------|-----------|------|------|
| `--onefile` | ~12 MB | Single file, easy to share | Slower startup |
| `--onedir` | ~15 MB | Faster startup | Multiple files |
| With UPX | ~8 MB | Smaller size | May trigger antivirus |

**Recommendation**: Use `--onefile` for easiest distribution!

---

## 🎯 **Complete Build Commands**

### **Basic Build:**
```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" src/main.py
```

### **With Icon:**
```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" --icon=icon.ico src/main.py
```

### **Clean Build (removes old files first):**
```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" --clean src/main.py
```

### **With Version Info (Windows):**
```bash
pyinstaller --onefile --windowed --name "RockPaperScissors" --version-file=version.txt src/main.py
```

---

## 📝 **After Building**

### **Test the Executable:**
1. Navigate to `dist/` folder
2. Double-click `RockPaperScissors.exe`
3. Test all features:
   - Single player works
   - Dark/light mode works
   - Multiplayer menus work
   - No errors appear

### **What to Upload to GitHub:**
- ✅ `RockPaperScissors.exe` (in Releases)
- ❌ Don't commit `build/` folder
- ❌ Don't commit `dist/` folder
- ❌ Don't commit `*.spec` files

Add to `.gitignore`:
```
# PyInstaller
build/
dist/
*.spec
```

---

## 🌟 **Professional Touch**

### **Create a README for Downloads:**

Create `DOWNLOAD_README.txt`:
```
🎮 Rock-Paper-Scissors Game
===========================

Thank you for downloading!

HOW TO RUN:
1. Double-click RockPaperScissors.exe
2. Choose your game mode
3. Enjoy!

FEATURES:
- Dark/Light mode toggle (moon/sun icon)
- Single player vs AI
- Wi-Fi multiplayer
- Beautiful modern UI

MULTIPLAYER:
- Both players need the game
- Must be on same Wi-Fi network
- One player hosts, other joins with IP

SYSTEM REQUIREMENTS:
- Windows 10 or later
- No Python needed!

TROUBLESHOOTING:
- If Windows Defender blocks it, click "More info" → "Run anyway"
- For multiplayer, allow through firewall when prompted

SOURCE CODE:
https://github.com/sammy440/Rock-Paper-Scissors-Game

Enjoy the game! 🎮
```

Include this with your executable!

---

## 🚀 **Quick Action Plan**

1. **Install PyInstaller**: `pip install pyinstaller`
2. **Build executable**: Run the command above
3. **Test it**: Make sure it works
4. **Create GitHub Release**: Upload the .exe
5. **Share the link**: Tell people where to download!

---

**Ready to build?** Run the command below to get started! 🎉

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "RockPaperScissors" src/main.py
```

Your executable will be in: `dist/RockPaperScissors.exe`
