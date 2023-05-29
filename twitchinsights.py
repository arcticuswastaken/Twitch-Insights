from typing import List
from tabulate import tabulate
import requests
from datetime import datetime, timezone
from os.path import exists

ALLOWED_BOTS_FILE = ".botsignore"

allowed_bots = []
if exists(ALLOWED_BOTS_FILE):
    allowed_bots = [bot.strip().lower() for bot in open(ALLOWED_BOTS_FILE, "r").readlines()]


print("Enter/Paste your content. Ctrl-C to save it.")
twitch_users = []
while True:
    try:
        line = input()
    except KeyboardInterrupt:
        break
    except EOFError:
        break
    twitch_users.append(line.strip().lower())
print("\n")

print("Checking the following users:")
for twitch_user in twitch_users:
    print(twitch_user)
print("\n")


# Get all bots
ret_all = requests.request(
    method="GET",
    url="https://api.twitchinsights.net/v1/bots/all",
)
twitchinsights_bots_all = ret_all.json()
all_bot_channels = set()
bots = {}
for bot in twitchinsights_bots_all["bots"]:
    (
        chanel,
        active_channels,
        last_seen,
    ) = bot
    all_bot_channels.add(chanel)
    bots[chanel] = [active_channels, last_seen]

# Get active bots
ret_active = requests.request(
    method="GET",
    url="https://api.twitchinsights.net/v1/bots/online",
)
twitchinsights_bots_active = ret_active.json()
active_bot_channels = set()
active_bots = {}
for bot in twitchinsights_bots_active["bots"]:
    (
        chanel,
        active_channels,
        last_seen,
    ) = bot
    active_bot_channels.add(chanel)
    active_bots[chanel] = [active_channels, last_seen]


potential_bots = set.intersection(all_bot_channels, set(twitch_users))
if len(potential_bots) == 0:
    print("No bots found!")
else:
    rows: List[List[str]] = []
    headers = [
        "Twitch Username",
        "Last Seen in x number of live channels",
        "Last Seen At",
    ]
    for bot in potential_bots:
        (
            active_channels,
            last_seen,
        ) = bots[bot]
        last_seen_datetime = datetime.fromtimestamp(last_seen, timezone.utc)
        if bot in active_bot_channels:
            last_seen_strftime = "Currently Online"
        else:
            last_seen_strftime = last_seen_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

        rows.append([bot, active_channels, last_seen_strftime])
    print(tabulate(rows, headers=headers))
print("\n")

input("Press Enter to exit...")
