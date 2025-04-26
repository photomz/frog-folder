#!/usr/bin/env bash
# Unload the launchd job
launchctl unload "$HOME/Library/LaunchAgents/com.markus.frogfolder.plist"

echo "Frog folder manager unloaded."
