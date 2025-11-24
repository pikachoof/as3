#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

command -v python3 >/dev/null 2>&1 && PYTHON_BIN="python3" || PYTHON_BIN="python"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to build the frontend" >&2
  exit 1
fi

echo "[backend] Installing dependencies from requirements.txt"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r "$BACKEND_DIR/requirements.txt"

echo "[frontend] Installing npm dependencies"
cd "$FRONTEND_DIR"
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi

echo "[frontend] Building production assets"
npm run build

echo "Build completed successfully"
