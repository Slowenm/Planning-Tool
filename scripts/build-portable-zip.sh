#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(grep '^version' "$ROOT/pyproject.toml" | head -1 | sed 's/.*"\(.*\)".*/\1/')"
NAME="Planning-Tool-${VERSION}-windows-portable"
OUT_DIR="$ROOT/dist"
ZIP="$OUT_DIR/${NAME}.zip"
STAGE="$OUT_DIR/$NAME"

rm -rf "$STAGE" "$ZIP"
mkdir -p "$STAGE"

copy_tree() {
  tar -C "$ROOT" \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='dist' \
    --exclude='schedule.md' \
    --exclude='schedule.ics' \
    --exclude='planning_tool.egg-info' \
    -cf - . | tar -C "$STAGE" -xf -
}

copy_tree

cd "$OUT_DIR"
zip -rq "${NAME}.zip" "$NAME"
rm -rf "$NAME"
echo "Created $ZIP"
ls -lh "$ZIP"
