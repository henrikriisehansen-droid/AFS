#!/bin/bash
# Build script for macOS standalone one-file executable

# Clean previous build artifacts
rm -rf build dist AFS-Validator.spec

# Run PyInstaller
# Switching to --onedir for better macOS bundle stability as recommended by PyInstaller
uv run pyinstaller --noconfirm --onedir --windowed --argv-emulation \
  --name "AFS-Validator" \
  --icon "icon/icon.icns" \
  --add-data "icon:icon" \
  --collect-all agentmail \
  --collect-all customtkinter \
  main.py

echo "Build complete! Check the dist folder."
