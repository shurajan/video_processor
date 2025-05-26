#!/bin/bash

set -e

VENV_DIR=".venv"
PEX_NAME="video_processor.pex"
PEX_TARGET="$HOME/.local/bin/${PEX_NAME}"
ENTRY_MODULE="main"
ENTRY_FUNCTION="main"

echo "📡 Pulling latest changes..."
git pull

# === Создание venv ===
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "📚 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade pex

echo "🛠 Creating bin directory..."
mkdir -p "$(dirname "$PEX_TARGET")"

echo "🔧 Building PEX into $PEX_TARGET"
pex . -r requirements.txt -e "${ENTRY_MODULE}:${ENTRY_FUNCTION}" -o "$PEX_TARGET"

deactivate
chmod +x "$PEX_TARGET"

echo "✅ Installed: $PEX_TARGET"
echo "🟢 Run from anywhere using: video_processor.pex"