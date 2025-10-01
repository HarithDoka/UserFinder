#!/bin/bash
# Installer Script for UserFinder Toolkit
# Author : NaldyDjafar
# Publisher : HarithDoka

echo "======================================="
echo "   🔎 Installing UserFinder Toolkit..."
echo "======================================="

# Update system
pkg update -y && pkg upgrade -y

# Install python & git
pkg install -y python git

# Install pip dependency
pip install requests

# Clone repo (kalau belum ada)
if [ ! -d "$HOME/UserFinder" ]; then
    git clone https://github.com/HarithDoka/UserFinder.git ~/UserFinder
fi

cd ~/UserFinder

echo "======================================="
echo " ✅ Installation complete!"
echo " ▶️ Run tool with: python userfinder.py"
echo "======================================="
