#!/bin/bash

set -e

VENV_DIR=".venv"
PEX_NAME="video_processor.pex"
PEX_TARGET="$HOME/.pex/$PEX_NAME"

echo "📡 Pulling latest changes..."
git pull

# === 1. Создание виртуального окружения ===
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# === 2. Установка pex
pip install --upgrade pip
pip install --upgrade pex build

# === 3. Сборка PEX с явным указанием точки входа
mkdir -p "$(dirname "$PEX_TARGET")"

echo "🔧 Building PEX → $PEX_TARGET"
pex . -o "$PEX_TARGET" --entry-point video_processor

deactivate
chmod +x "$PEX_TARGET"

echo "✅ Installed to: $PEX_TARGET"

# === 4. Подсказка по добавлению в PATH
if [[ ":$PATH:" != *":$HOME/.pex:"* ]]; then
  echo
  echo "ℹ️  To run from anywhere, add this to your shell config:"
  echo 'export PATH="$HOME/.pex:$PATH"'
fi