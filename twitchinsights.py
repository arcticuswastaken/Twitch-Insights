from typing import List
from tabulate import tabulate
import requests
from datetime import datetime, timezone

datetime_now = datetime.now(timezone.utc)

print("Enter/Paste your content. Ctrl-C to save it.")
twitch_users = []
while True:
    try:
        line = input()
    except KeyboardInterrupt:
        break
    except EOFError:
        break
    twitch_users.append(line.lower().strip())
print("\n")

print("Checking the following users:")
for twitch_user in twitch_users:
    print(twitch_user)
print("\n")

ret = requests.request(
    method="GET",
    url="https://api.twitchinsights.net/v1/bots/all",
)
twitchinsights = ret.json()
bot_channels = set()
bots = {}
for bot in twitchinsights["bots"]:
    (
        chanel,
        active_channels,
        last_seen,
    ) = bot
    bot_channels.add(chanel)
    bots[chanel] = [active_channels, last_seen]
potential_bots = set.intersection(bot_channels, set(twitch_users))
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
        if last_seen_datetime > datetime_now:
            last_seen_strftime = "Currently Online"
        else:
            last_seen_strftime = last_seen_datetime.strftime("%a, %d %b %Y %H:%M:%S GMTE")

        rows.append([bot, active_channels, last_seen_strftime])
    print(tabulate(rows, headers=headers))
print("\n")

input("Press Enter to exit...")
