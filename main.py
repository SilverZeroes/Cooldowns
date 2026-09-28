import time
import json

cooldown = 10 # 10 seconds

"""
start = time.time()
remaining = max(0, cooldown - (time.time() - start))
while remaining > 0:
    remaining = max(0, cooldown - (time.time() - start))

    print(int(remaining))

    time.sleep(1)
"""



data = {
    "start_time": 1790608446.8012552,
    "cooldown": 4 * 24 * 60 * 60
}




with open("./cooldown.json", "r") as f:
    prompt = json.load(f)

    remaining = max(0, data["cooldown"] - (time.time() - data["start_time"]) )

    days = int(remaining // 86400)
    hours = int((remaining % 86400)// 3600)
    minutes = int((remaining % 3600) // 60)
    seconds = int(remaining % 60)

    print(f"Remaining time {days} days and {hours:02} hours and {minutes:02} minutes and {seconds:02} seconds.")
    print(f"Remaining time {days} - {hours:02}:{minutes:02}:{seconds:02}.")






