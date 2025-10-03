#!/bin/bash

echo "===================================="
echo "Building OrbitaApp"
echo "===================================="
echo

# Activate virtual environment
source venv/bin/activate

# Install PyInstaller if not installed
pip install -r requirements.txt

# Clean previous builds
rm -rf build dist

# Build the executable
pyinstaller app.spec

echo
echo "===================================="
echo "Build complete!"
echo "Executable is in: dist/OrbitaApp"
echo "===================================="
echo