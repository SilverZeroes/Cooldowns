import os
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

def reset_data(entry: dict) -> None:
    entry["start_time"] = time.time()

def total_seconds(days: int, hours: int, minutes: int, seconds: int) -> int:
    return (
        days * SECONDS_PER_DAY +
        hours * SECONDS_PER_HOUR +
        minutes * SECONDS_PER_MINUTE +
        seconds
    )

def add_entry() -> None:
    name = input("Enter timer name: ")

    # Name validation.
    if not name.strip():
        print("Name cannot be empty.")
        return
    if any(entry["name"] == name for entry in data):
        print("An event with this name already exists.")
        return
    name = name.strip()

    # The user has the liberty to say 1 and minus 4 hours as long as the end duration is positive.
    days = int(input("Enter amount of days: "))
    hours = int(input("Enter amount of hours: "))
    minutes = int(input("Enter amount of minutes: "))
    seconds = int(input("Enter amount of seconds: "))

    duration = abs(total_seconds(days, hours, minutes, seconds))

    data.append({
        "name": name,
        "start_time": time.time(),
        "cooldown": duration
    })
    
    save_data(PATH, data)

def remove_entry() -> None:
    print("Name")
    for entry in data:
        display_timer(entry)
     
    name = input("\nChoose an entry to delete: ")

    for entry in data:
            if name == entry["name"]:
                print("Entry found, removing...")
                data.remove(entry)
                save_data(PATH, data)

def reset_entry() -> None:
    print("Name")
    for entry in data:
        display_timer(entry)

    name = input("\nChoose an entry to reset: ")

    for entry in data:
        if name == entry["name"]:
            print("Entry found, reseting...")
            reset_data(entry)
            save_data(PATH, data)


def display_timer(entry: dict) -> None:

    remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )

    days = int(remaining // SECONDS_PER_DAY)
    hours = int((remaining % SECONDS_PER_DAY)// SECONDS_PER_HOUR)
    minutes = int((remaining % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
    seconds = int(remaining % SECONDS_PER_MINUTE)

    # print(f"Remaining time {days} days and {hours:02} hours and {minutes:02} minutes and {seconds:02} seconds.")
    print(f"{entry["name"] + ":":15}{days} - {hours:02}:{minutes:02}:{seconds:02}.")


def live_preview() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        for entry in data:
            display_timer(entry)
            remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )
            if remaining <= 0:
                # print(f"Cooldown duration for '{entry["name"]}' over, reseting now...")
                reset_data(entry)
                save_data(PATH, data)
        time.sleep(1)

if __name__ == "__main__":
    data = load_data(PATH)
    if len(argv) > 1 and argv[1] == "add":
        add_entry()
        exit()
    elif len(argv) > 1 and argv[1] == "remove":
        remove_entry()
        exit()
    elif len(argv) > 1 and argv[1] == "reset":
        reset_entry()
        exit()
    elif len(argv) > 1 and argv[1] == "live":
            live_preview()
            exit()
    

    changed = False
    
    for entry in data:
            remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )
    
            if remaining <= 0:
                print(f"Cooldown duration for '{entry["name"]}' over, reseting now...")
                reset_data(entry)
                changed = True

    for entry in data:
        display_timer(entry)

    if changed:
         save_data(PATH, data)
