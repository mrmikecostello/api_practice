import json
import requests
from character_names_dict import *

# character_info.py
# This file will access the character inventory of a player and list information about specified
# characters.
# 7/17/2020: Version pulls character inventory and displays basic info using the API.
# 7/18/2020: This will be able to pull directly from the API but will use a local copy to limit
# calls to the API. Future versions will also pull spell data. Imports character name/id dictionary
# from external file. Added input for testing purposes. Deploying version to bot.

#7/18/2020: API Access is turned off temporarily to limit calls
api_token = '5ff5e529-fb38-4f36-9893-307858eec8f5'
api_url_base = 'https://dsa.fan/api/players/7A0F3549'
headers = {'HTTP-X-API-IDENTIFIER': api_token}
# #
## Pull data with API and create dictionary
data_request = requests.get(api_url_base, headers=headers)

## Open local copy of data for use with this program - NOT WORKING!!!!
# 7/18/2020: Tried a bunch of ways to do this and it would not parse the JSON properly.
# Opening JSON file
#with open('player_data.json') as json_file:
#    full_data = json.load(json_file)
# with open('player_data.json', 'r') as myfile:
#     data_request=myfile.read()
# # returns JSON object as a dictionary
#full_data = json.loads(data)
# # Closing file
#myfile.close()

# Convert data pulled from API to dictionary
full_data = json.loads(data_request.content)
# 7/18/2020: Create Dictionary of all Character Inventory Information. Other dictionaries could
# be quickly created from initial data dump. Need to figure out a way to keep data cached to limit
# number of hits to the API.
if full_data['player'] != None:
    current_character = full_data['player']['unitInventory']
else:
    print("nope")
    quit()

while True:    # infinite loop
    pick = input("\nWhich character?: ")
    if pick == "q":
        break  # stops the loop
    else:

        find_char = next((item for item in character_names if item['name'] == pick), None)
        found_char = find_char['definitionId']
#print(find_char)
#print(found_char)

        character_dict = next((item for item in current_character if item['definitionId'] == found_char), None)

        print(find_char['name'])
        print('Rarity:',character_dict['rarity'],'stars')
        print('Level:',character_dict['level'])
        print('Gear Tier:',character_dict['gearTier'])
        if (character_dict['sorcererStoneId'] > 0):
            print('Sorcerer Stone: Yes')
        else:
            print('Sorcerer Stone: No')
        print('Power:',character_dict['powerRating'])
        print()

print("\nComplete.")

