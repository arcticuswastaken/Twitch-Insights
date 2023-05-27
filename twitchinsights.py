import requests

print("Enter/Paste your content. Ctrl-C to save it.")
twitch_users = []
while True:
    try:
        line = input()
    except KeyboardInterrupt:
        break
    except EOFError:
        break
    twitch_users.append(line.lower())
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
    chanel, active_channels, last_seen = bot
    bot_channels.add(chanel)
    bots[chanel] = [active_channels, last_seen]
potential_bots = set.intersection(bot_channels, set(twitch_users))
if (len(potential_bots) == 0):
    print("No bots found!")
else:
    heading_sizes = [0, 0, 0]
    heading_names = ["Name", "Active", "Last Seen"]
    heading_paddings = [0, 0, 0]

    for bot in potential_bots:
        active_channels, last_seen = bots[bot]
        if heading_sizes[0] < len(bot):
            heading_sizes[0] = len(bot)
        if heading_sizes[1] < len(str(active_channels)):
            heading_sizes[1] = len(str(active_channels))
        if heading_sizes[2] < len(str(last_seen)):
            heading_sizes[2] = len(str(last_seen))
 
    for i in range(len(heading_names)):
        padding = (heading_sizes[i] - len(heading_names[i]))
        if padding < 1:
            padding = 0
        if padding % 2:
            padding = int((padding + 1)/2)
        else:
            padding = int(padding/2)
        heading_paddings[i] = padding + 1

    heading = f'{" "*heading_paddings[0]}{heading_names[0]}{" "*heading_paddings[0]}{" "*heading_paddings[1]}{heading_names[1]}{" "*heading_paddings[1]}{" "*heading_paddings[2]}{heading_names[2]}{" "*heading_paddings[2]}'
    print(heading)
    for bot in potential_bots:
        active_channels, last_seen = bots[bot]
        name_padding = heading_paddings[0] - len(bot)
        active_padding = heading_paddings[1] - len(str(active_channels))
        last_seen_padding = heading_paddings[2] - len(str(last_seen))
        if name_padding < 1:
            name_padding = 1
        if active_padding < 1:
            active_padding = 1
        if last_seen_padding < 1:
            last_seen_padding = 1
        row = f'{" "*name_padding}{bot}{" "*name_padding}{" "*active_padding}{active_channels}{" "*active_padding}{" "*last_seen_padding}{last_seen}{" "*last_seen_padding}'
        print(row)
print("\n")

input("Press Enter to exit...")