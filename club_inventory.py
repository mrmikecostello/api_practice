import json
import requests
import aiohttp
import asyncio
import os
from character_names_dict import *

selected_character = 5239884894495182

# club_inventory.py
# Originally named club_character.py
# This file will access the character inventory of every player from a club and list information about specified
# characters for each player.
# 7/21/2020: This initial version is based on character_info.py.
#   This version will use a variable to determine the character (or spell eventually) to be queried.
#   It will generate a list of club members with their Player IDs.
#   The list will be used to loop through the entire guild and pull out the character information for each
#   member of the club.
# 8/4/2020: Rebuilding to take advantage of asyncio
# 8/18/2020: Attempting to cache requests.

# API Access
api_token = '5ff5e529-fb38-4f36-9893-307858eec8f5'
api_url_base = 'https://dsa.fan/api/'
club_id = '1781C0AB' #fantasyland
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
#club_member_list = [{'id':member['player']['id'],'username':member['player']['username']} for member in club_roster]
players = [{'id':member['player']['id'],'username':member['player']['username']} for member in club_roster]

club_character_inventory = []
club_character_locked = []

#print(club_member_list)

#players = [{'id': 'AFDF2E95', 'username': 'SrSparkles'}, {'id': 'BCD2D9DB', 'username': 'Ladyianto'}, {'id': 'C25FCF73', 'username': 'LordFarquaad'}]

async def fetch(session, player_api_url):
    """Execute an http call async
    Args:
        session: context for making the http call
        url: URL to call
    Return:
        responses: A dict like object containing http response
    """
    async with session.get(player_api_url, headers=headers) as response:
        resp = await response.json()
        current_player = resp['player']['unitInventory']
        character_dict = next((item for item in current_player if item['definitionId'] == selected_character), None)
        try:
            player_dict = {'id': resp['player']['id'], 'username': resp['player']['username'], 'unlocked': 'T',
            'rarity':character_dict['rarity'], 'level':character_dict['level'], 'gearTier':character_dict['gearTier'],
            'sorcererStoneId':character_dict['sorcererStoneId'],'powerRating':character_dict['powerRating']}
        except TypeError:
            player_dict = {'id':resp['player']['id'], 'username':resp['player']['username'], 'unlocked': 'F',}

        return player_dict

async def fetch_all(players):
    """ Gather many HTTP call made async
    Args:
        cities: a list of string
    Return:
        responses: A list of dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for member in players:
            player_api_url = api_url_base + "players/" + member['id']
            tasks.append(
                fetch(
                    session,
                    player_api_url,
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

def run(players):
    responses = asyncio.run(fetch_all(players))
 #   return responses
    for entry in responses:
        print(entry)



# for member in players:
# #for member in club_member_list:
#     ## Take player id from dictionary entry in the list and build player_api_url
#     player_api_url = api_url_base + "players/" + member['id']
#     ## Pull player information with API
#     player_request = requests.get(player_api_url, headers=headers)
#     player_data = json.loads(player_request.content)
#     current_player = player_data['player']['unitInventory']
# #    print(player_api_url)
#     character_dict = next((item for item in current_player if item['definitionId'] == selected_character), None)
#
#     try:
#         club_character_inventory.append({'id': member['id'], 'username': member['username'],
#         'rarity':character_dict['rarity'], 'level':character_dict['level'], 'gearTier':character_dict['gearTier'],
#         'sorcererStoneId':character_dict['sorcererStoneId'],'powerRating':character_dict['powerRating']})
#     except TypeError:
#         club_character_locked.append({'id':member['id'], 'username':member['username']})
#
# ## Sort club_character_inventory and club_character_locked ascending by alphabetical
# club_character_inventory = sorted(club_character_inventory, key = lambda i: (i['username']).lower())
# club_character_locked = sorted(club_character_locked, key = lambda i: (i['username']).lower())
#
# ## Print list of players with the character unlocked and locked
# find_char = next((item for item in character_names if item['definitionId'] == selected_character), None)
# print('Club Inventory for',find_char['name'],'for',club_name)
# print()
#
# print('Players with Character Unlocked:', len(club_character_inventory))
# for player in club_character_inventory:
#     print(player['username'], '-', player['rarity'], 'stars, Level:',player['level'], end = ', ')
#     print('Gear Tier:',player['gearTier'], end =', ')
#     if (player['sorcererStoneId'] > 0):
#         print('Sorcerer Stone: Yes', end =', ')
#     else:
#         print('Sorcerer Stone: No', end =', '),
#     print('Power:',player['powerRating'])
#
# print()
# print('Players with Character Locked:', len(club_character_locked))
# for player in club_character_locked:
#     print(player['username'])

run(players)

print("\nComplete.")

