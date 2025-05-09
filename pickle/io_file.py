import pickle

with open('dj.life', 'wb') as file:
    pickle.dump({'dj': 'life'}, file)

with open('dj.life', 'rb') as file:
    djlife = pickle.load(file)

print(djlife)