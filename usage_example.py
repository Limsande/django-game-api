import requests

URL = 'http://127.0.0.1:8000/games/'
IDS = []


def prettify_game(json: dict) -> str:
    return f'{json["title"]} by {json["studio"]}: {json["description"]}'


print('--- POST some new games ---')
new_games = [
    {'title': 'The Witcher 3', 'studio': 'CDPR', 'description': 'Like lilac and gooseberries'},
    {'title': 'Cyberpunkt 2077', 'studio': 'CDPR', 'description': 'What a ride'},
    {'title': 'Horizon Zero Dawn', 'studio': 'Guerrilla', 'description': 'Otherworldly'}
]
for game in new_games:
    response = requests.post(URL, data=game)
    print('Created', prettify_game(response.json()))

print('\n--- GET all games ---')
response = requests.get(URL)
for i, game in enumerate(response.json()):
    print(f'{i+1}#:', prettify_game(game))
    IDS.append(game['id'])

print('\n--- GET a single game ---')
response = requests.get(URL + str(IDS[-1]))
print(prettify_game(response.json()))

print('\n--- PUT an updated game ---')
game = requests.get(URL + str(IDS[0])).json()
game['description'] = 'Wind\'s howling'
response = requests.put(URL + str(game['id']), data=game)
print('Updated game:', prettify_game(response.json()))

print('\n--- DELETE all games ---')
for game in requests.get(URL).json():
    requests.delete(URL + str(game['id']))
    print('Deleted game with ID', str(game['id']))
