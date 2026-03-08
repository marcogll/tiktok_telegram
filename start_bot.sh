#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source .venv/bin/activate

echo "🤖 Iniciando bot de redes sociales..."
exec python3 social_downloader.py
