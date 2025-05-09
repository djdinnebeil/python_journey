import json

with open('dj.life', 'w') as file:
    json.dump({'dj': 'life'}, file)

with open('dj.life', 'r') as file:
    djlife = json.load(file)

print(djlife)