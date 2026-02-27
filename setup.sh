#!/bin/bash

# VULNETT SECURITY SYSTEMS - DEPLOYMENT SCRIPT
# Target OS: Linux (Debian/Ubuntu/Kali)

# Ensure we are in the script's directory
cd "$(dirname "$0")"

echo "🚀 Starting Vulnett Environment Initialization..."

# 1. Update System
sudo apt update

# 2. Install Core System Tools
echo "[+] Installing System Tools (nmap, python3-venv, wget, unzip)..."
sudo apt install -y nmap python3-venv python3-pip wget unzip

# 3. Install Nuclei (v3.7.0 stable)
if ! command -v nuclei &> /dev/null
then
    ARCH=$(uname -m)
    case $ARCH in
        x86_64)  NUCLEI_ARCH="amd64" ;;
        aarch64) NUCLEI_ARCH="arm64" ;;
        *)       NUCLEI_ARCH="amd64" ;;
    esac
    echo "[+] Detected architecture: $ARCH. Downloading Nuclei v3.7.0 for $NUCLEI_ARCH..."
    TEMP_DIR=$(mktemp -d)
    wget "https://github.com/projectdiscovery/nuclei/releases/download/v3.7.0/nuclei_3.7.0_linux_${NUCLEI_ARCH}.zip" -O "$TEMP_DIR/nuclei.zip"
    unzip "$TEMP_DIR/nuclei.zip" -d "$TEMP_DIR"
    chmod +x "$TEMP_DIR/nuclei"
    sudo mv "$TEMP_DIR/nuclei" /usr/local/bin/
    rm -rf "$TEMP_DIR"
    echo "[*] Nuclei installed successfully."
else
    echo "[*] Nuclei already installed. Skipping."
fi

# 4. Set up Python Virtual Environment
VENV_PYTHON=".venv/bin/python3"
if [ ! -f "$VENV_PYTHON" ]; then
    VENV_PYTHON=".venv/Scripts/python.exe" # Cross-platform check
fi

# Auto-repair corrupted venv
if [ -d ".venv" ] && [ ! -f "$VENV_PYTHON" ]; then
    echo "[!] Existing .venv appears corrupted. Re-initializing..."
    rm -rf .venv
fi

if [ ! -d ".venv" ]; then
    echo "[+] Creating Python Virtual Environment (using copies for portability)..."
    python3 -m venv .venv --copies
fi

# 5. Install Python Dependencies
echo "[+] Installing Python Packages..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. Final Instructions
echo ""
echo "✅ DEPLOYMENT COMPLETE"
echo "--------------------------------------"
echo "To start the gateway:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Add your ngrok token (once per setup): ngrok config add-authtoken YOUR_TOKEN"
echo "3. Run the script: python3 scanner.py"
echo "--------------------------------------"
