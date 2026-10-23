#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/offline/wheels"
mkdir -p "$DEST"
rm -f "$DEST"/*

# Windows / Python 3.11 wheels for conda env planning-tool
python3 -m pip download -d "$DEST" \
  -r "$ROOT/offline/requirements.txt" \
  --platform win_amd64 \
  --python-version 3.11 \
  --implementation cp \
  --only-binary=:all: \
  2>/dev/null || true

# Pure-Python / tzdata may lack win-specific wheel tag; allow any
python3 -m pip download -d "$DEST" \
  openpyxl icalendar tzdata setuptools wheel \
  --no-deps \
  2>/dev/null || true

python3 -m pip download -d "$DEST" \
  pywin32 \
  --platform win_amd64 \
  --python-version 3.11 \
  --only-binary=:all: \
  2>/dev/null || true

echo "Wheels in $DEST:"
ls -la "$DEST" | tail -20
COUNT="$(find "$DEST" -name '*.whl' | wc -l)"
if [ "$COUNT" -lt 4 ]; then
  echo "WARNING: expected several wheels, got $COUNT"
  exit 1
fi
