#!/bin/bash
# Install all requirements in the current virtual environment

set -e

echo "Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel

echo "Installing project requirements..."
python3 -m pip install -r requirements.txt

echo "✅ Requirements installed successfully."
