#!/usr/bin/env bash
set -e

MANAGER_DIR="$HOME/Code/frog-folder"
PLIST_SRC="$MANAGER_DIR/com.markus.frogfolder.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.markus.frogfolder.plist"

# Ensure YAML parser is installed
pip3 install --user pyyaml

# Prepare directories
mkdir -p "$MANAGER_DIR"
mkdir -p "$HOME/Library/LaunchAgents"

# Copy plist into LaunchAgents
cp "$PLIST_SRC" "$PLIST_DST"

# Load or reload the agent
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load   "$PLIST_DST"

echo "Dynamic symlink manager installed and loaded."