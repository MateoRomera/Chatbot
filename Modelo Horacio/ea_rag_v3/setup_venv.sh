#!/bin/bash
# Setup local virtual environment for ea_rag_v3

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "📦 Setting up virtual environment in: $VENV_DIR"

# Create venv if it does not exist
if [ ! -d "$VENV_DIR" ]; then
    echo "➡️ Creating new virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Virtual environment already exists."
fi

# Activate venv
echo "➡️ Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip/setuptools/wheel
echo "⬆️ Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel

# Install project dependencies
echo "📥 Installing requirements..."
python3 -m pip install -r "$PROJECT_DIR/requirements.txt"

echo "🎉 Virtual environment ready."
echo "To activate later, run:"
echo "    source .venv/bin/activate"
