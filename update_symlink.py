#!/usr/bin/env python3
import sys
import yaml
import datetime
import os
from pathlib import Path
import tempfile
from typing import Dict, Any

# Paths
MANAGER_DIR = Path.home() / "Code" / "frog-folder"
CONFIG_FILE = MANAGER_DIR / "config.yaml"
CONFIG_KEY = "y1q3"
BASE_DIR = Path.home() / "Code" / "stanford"
LINK_PATH = Path.home() / "Desktop" / "🐸"
FALLBACK = Path.home() / "Code" / "stanford"


def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)[CONFIG_KEY] or {}
    except Exception as e:
        print(f"Error loading config file: {e}", file=sys.stderr)
        return {}


def get_target(config: Dict[str, Any]) -> Path:
    now = datetime.datetime.now()
    day = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    day_schedule = config.get(day, {})

    best_start_time = None
    best_folder = None

    for time_slot, folder in day_schedule.items():
        print(time_slot, folder)
        try:
            start_time, end_time = time_slot.split("/", 1)
            if start_time <= current_time <= end_time:
                if best_start_time is None or start_time > best_start_time:
                    best_start_time = start_time
                    best_folder = folder
        except ValueError:
            print(f"Error splitting time slot: {time_slot}", file=sys.stderr)
            continue

    if best_folder:
        return BASE_DIR / best_folder

    default_folder = config.get("_default")
    return BASE_DIR / default_folder if default_folder else FALLBACK


def update_symlink(target: Path) -> None:
    if not target.is_dir():
        target = FALLBACK

    if LINK_PATH.is_symlink():
        current = LINK_PATH.readlink()
        if current.resolve() == target.resolve():
            return

    temp_link = None
    try:
        dir_name = LINK_PATH.parent
        fd, temp_path = tempfile.mkstemp(dir=dir_name)
        os.close(fd)
        Path(temp_path).unlink()
        temp_link = Path(temp_path)
        temp_link.symlink_to(target)
        temp_link.replace(LINK_PATH)
    except Exception as e:
        print(f"Error updating symlink: {e}", file=sys.stderr)
        if temp_link and temp_link.exists():
            temp_link.unlink()


def main() -> None:
    config = load_config()
    target = get_target(config)
    update_symlink(target)


if __name__ == "__main__":
    main()
