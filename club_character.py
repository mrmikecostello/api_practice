import json
import requests
import timeit
from character_names_dict import *
import requests_cache

requests_cache.install_cache('cache/dsa_cache', backend='sqlite', expire_after=300)

selected_character = 5584717432624453

# club_character.py
# This file will access the character inventory of every player from a club and list information about specified
# characters for each player.
# 7/21/2020: This initial version is based on character_info.py.
#   This version will use a variable to determine the character (or spell eventually) to be queried.
#   It will generate a list of club members with their Player IDs.
#   The list will be used to loop through the entire guild and pull out the character information for each
#   member of the club.

# API Access
api_token = '5ff5e529-fb38-4f36-9893-307858eec8f5'
api_url_base = 'https://dsa.fan/api/'
club_id = '1781C0AB'
club_api_url = api_url_base + "clubs/" + club_id
headers = {'HTTP-X-API-IDENTIFIER': api_token}

## Pull full club data with API
data_request = requests.get(club_api_url, headers=headers)

# Convert data pulled from API to dictionary
full_data = json.loads(data_request.content)
# Create dictionary of player information from club roster.
club_roster = full_data['club']['roster']
club_name = full_data['club']['name']
# Create list of dictionaries of player ids and usernames
club_member_list = [{'id':member['player']['id'],'username':member['player']['username']} for member in club_roster]

club_character_inventory = []
club_character_locked = []

for member in club_member_list:
    requests_cache.install_cache('cache/' + member['id'], backend='sqlite', expire_after=300)
    ## Take player id from dictionary entry in the list and build player_api_url
    player_api_url = api_url_base + "players/" + member['id']
    ## Pull player information with API
    player_request = requests.get(player_api_url, headers=headers)
    player_data = json.loads(player_request.content)
    current_player = player_data['player']['unitInventory']
#    print(player_api_url)
    character_dict = next((item for item in current_player if item['definitionId'] == selected_character), None)

    try:
        club_character_inventory.append({'id': member['id'], 'username': member['username'],
        'rarity':character_dict['rarity'], 'level':character_dict['level'], 'gearTier':character_dict['gearTier'],
        'sorcererStoneId':character_dict['sorcererStoneId'],'powerRating':character_dict['powerRating'],'cache':str(data_request.from_cache)})
    except TypeError:
        club_character_locked.append({'id':member['id'], 'username':member['username'],'cache':str(data_request.from_cache)})


## Sort club_character_inventory and club_character_locked ascending by alphabetical
club_character_inventory = sorted(club_character_inventory, key = lambda i: (i['username']).lower())
club_character_locked = sorted(club_character_locked, key = lambda i: (i['username']).lower())

## Print list of players with the character unlocked and locked
find_char = next((item for item in character_names if item['definitionId'] == selected_character), None)
print('Club Inventory for',find_char['name'],'for',club_name)
print()

print('Players with Character Unlocked:', len(club_character_inventory))
for player in club_character_inventory:
    print(player['username'], '-', player['rarity'], 'stars, Level:',player['level'], end = ', ')
    print('Gear Tier:',player['gearTier'], end =', ')
    if (player['sorcererStoneId'] > 0):
        print('Sorcerer Stone: Yes', end =', ')
    else:
        print('Sorcerer Stone: No', end =', '),
    print('Power:',player['powerRating'], end =', ')
    print('Cache:',player['cache'])

print()
print('Players with Character Locked:', len(club_character_locked))
for player in club_character_locked:
    print(player['username'], end =', ')
    print('Cache:', player['cache'])



print("\nComplete.")

