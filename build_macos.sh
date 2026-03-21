#!/bin/bash
# Build script for macOS standalone one-file executable

# Clean previous build artifacts
rm -rf build dist AFS-Validator.spec

# Run PyInstaller
# Using --collect-all for flet and agentmail
uv run pyinstaller --noconfirm --onedir --windowed --argv-emulation \
  --name "AFS-Validator" \
  --icon "icon/icon.icns" \
  --add-data "icon:icon" \
  --add-data "config.example.toml:." \
  --collect-all flet \
  --collect-all agentmail \
  main.py

echo "Build complete! Check the dist folder."
