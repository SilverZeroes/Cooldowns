import time
import json
from pathlib import Path


SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400


# data = {
#     "start_time": 1790608446.8012552,
#     "cooldown": 10
# }

path = Path("cooldown.json")

def display_timer(entry: dict) -> None:

    remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )

    days = int(remaining // SECONDS_PER_DAY)
    hours = int((remaining % SECONDS_PER_DAY)// SECONDS_PER_HOUR)
    minutes = int((remaining % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
    seconds = int(remaining % SECONDS_PER_MINUTE)

    # print(f"Remaining time {days} days and {hours:02} hours and {minutes:02} minutes and {seconds:02} seconds.")
    print(f"{entry["name"] + ":":15} Remaining time {days} - {hours:02}:{minutes:02}:{seconds:02}.")

with open(path, "r") as f:
    changed = False
    data = json.load(f)
    for entry in data:
        remaining = max(0, entry["cooldown"] - (time.time() - entry["start_time"]) )

        if remaining <= 0:
            print(f"Cooldown duration for '{entry["name"]}' over, reseting now...")
            entry["start_time"] = time.time()
            changed = True

    for entry in data:
         display_timer(entry)

    if changed:    
        with open(path, "w") as f:
                json.dump(data, f)
            # remaining = max(0, data["cooldown"] - (time.time() - data["start_time"]) )


    
    

# days = int(remaining // 86400)
# hours = int((remaining % 86400)// 3600)
# minutes = int((remaining % 3600) // 60)
# seconds = int(remaining % 60)

# print(f"Remaining time {days} days and {hours:02} hours and {minutes:02} minutes and {seconds:02} seconds.")
# print(f"Remaining time {days} - {hours:02}:{minutes:02}:{seconds:02}.")






