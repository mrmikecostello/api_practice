import requests

url = 'https://dsa.fan/guilds/top-guilds/total_summoner_score'
r = requests.get(url)

top100list = []

for line in r.text.splitlines():
    if "<td><a href=\"/guilds/" in line:
        startpoint = line.find("guilds") + 7
        top100list.append(line[startpoint:startpoint+8])

print(top100list, len(top100list))