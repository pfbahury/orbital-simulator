@echo off
echo ====================================
echo Building OrbitaApp.exe
echo ====================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install depedencies if not installed
pip install -r requirements.txt

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
pyinstaller app.spec

echo.
echo ====================================
echo Build complete!
echo Executable is in: dist\OrbitaApp.exe
echo ====================================
echo.

pause