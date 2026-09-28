import time
import json
from sys import argv
from pathlib import Path


SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400

BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "cooldown.json"

def load_data(path: Path) -> list:
    with open(path, "r") as f:
        data = json.load(f)
    return data

def save_data(path: Path, data: list) -> list:
     with open(path, "w") as f:
        json.dump(data, f)

def add_entry() -> None:
     pass

def remove_entry() -> None:
     pass

def display_timer(entry: dict) -> None:

    remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )

    days = int(remaining // SECONDS_PER_DAY)
    hours = int((remaining % SECONDS_PER_DAY)// SECONDS_PER_HOUR)
    minutes = int((remaining % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
    seconds = int(remaining % SECONDS_PER_MINUTE)

    # print(f"Remaining time {days} days and {hours:02} hours and {minutes:02} minutes and {seconds:02} seconds.")
    print(f"{entry["name"] + ":":15}{days} - {hours:02}:{minutes:02}:{seconds:02}.")


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == "add":
         add_entry()
         exit()
    elif len(argv) > 1 and argv[1] == "remove":
         remove_entry()
         exit()
    

    changed = False
    data = load_data(PATH)
    for entry in data:
            remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )
    
            if remaining <= 0:
                print(f"Cooldown duration for '{entry["name"]}' over, reseting now...")
                entry["start_time"] = time.time()
                changed = True

    for entry in data:
        display_timer(entry)

    if changed:
         save_data(PATH, data)
