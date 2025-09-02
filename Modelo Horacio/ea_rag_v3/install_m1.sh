#!/bin/bash
# Installer for ea_rag_v3 on Apple Silicon (M1/M2)

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "📦 Setting up environment for ea_rag_v3 (Apple Silicon)..."

# Ensure virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "➡️ Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
echo "➡️ Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip/setuptools/wheel
echo "⬆️ Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel

# Install PyTorch from Apple Silicon channel
echo "🧠 Installing PyTorch (CPU/MPS for Apple Silicon)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other project requirements (without re-fetching torch)
echo "📥 Installing project requirements..."
pip install -r "$PROJECT_DIR/requirements.txt" --no-deps

echo "✅ Installation complete!"
echo
echo "To start working, activate your environment with:"
echo "    source .venv/bin/activate"
echo
