import json
import requests

# This file will access the API and download the current player data for my account
# and the current club data for Awakened. It will save the data as a text file for
# reference use.

api_token = '5ff5e529-fb38-4f36-9893-307858eec8f5'
#player_url_base = 'https://dsa.fan/api/players/7A0F3549' #CrazyOldOswald
player_url_base = 'https://dsa.fan/api/players/7A0F0534' #Maelstrom
#player_url_base = 'https://dsa.fan/api/players/61863B98' #BigJohnnyK
#club_url_base = 'https://dsa.fan/api/clubs/BCD2D1CB'  # Awakened
club_url_base = 'https://dsa.fan/api/clubs/77197E18'  # MsM
character_data_api_url = 'https://dsa.fan/api/characters'

headers = {'HTTP-X-API-IDENTIFIER': api_token}

player_request = requests.get(player_url_base, headers=headers)
club_request = requests.get(club_url_base, headers=headers)
characters_request = requests.get(character_data_api_url, headers=headers)

#player_data = open("player_data.txt", "w")
player_data = open("maelstrom_player_data.txt", "w")
player_data.write(str(player_request.content))
player_data.close()

# player_data_json = open("player_data.json", "w")
# player_data_json.write(str(player_request.content))
# player_data_json.close()

with open('player_data.json', 'w') as outfile:
    json.dump(str(player_request.content), outfile)

club_data = open("club_data.txt", "w")
club_data.write(str(club_request.content))
club_data.close()

# 8663828779652044 - id for ursula ticket

# characters_data = open("characters_data.txt", "w")
# characters_data.write(str(characters_request.content))
# characters_data.close()

# characters_data_dict = json.loads(characters_request.content)
# print(characters_data_dict.keys())

print("Complete.")

