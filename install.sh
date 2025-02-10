#!/bin/sh

# Check for Internet connection

if ! ping -c 1 google.com >/dev/null 2>&1; then
  echo "[-] No internet connection. Please check your network settings."
  exit 1
fi

# Check if uv is installed
if command -v uv &>/dev/null; then
  echo "[+] uv is already installed. Skipping installation."
else
  echo "[+] Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Resolve dependencies
echo "[+] Resolving dependencies..."
uv sync



# Done
echo "[+] To run Mindful, run the command:"
echo "uv run server_launch.py"
