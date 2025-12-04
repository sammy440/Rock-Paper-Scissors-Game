@echo off
echo ========================================
echo Building Rock-Paper-Scissors Game
echo ========================================
echo.

echo [1/3] Installing PyInstaller...
pip install pyinstaller
echo.

echo [2/3] Building executable...
echo This may take a few minutes...
pyinstaller --onefile --windowed --name "RockPaperScissors" --clean --paths=src src\main.py
echo.

echo [3/3] Cleaning up...
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located at:
echo %CD%\dist\RockPaperScissors.exe
echo.

if exist "dist\RockPaperScissors.exe" (
    echo File size:
    dir dist\RockPaperScissors.exe | find "RockPaperScissors.exe"
    echo.
    echo ✓ Build successful!
    echo.
    echo Testing the executable...
    start "" "dist\RockPaperScissors.exe"
    echo.
    echo Next steps:
    echo 1. Test the executable (should have opened)
    echo 2. Create a GitHub Release
    echo 3. Upload the .exe file
    echo 4. Share the download link!
) else (
    echo ✗ Build failed! Check the error messages above.
)

echo.
pause
