import json
import io

with open('dj.life', 'w') as file: # type: io.IOBase
    json.dump(({'dj': 'life', 'arr1': [1,2,3]}, 5), file, indent=2)

with open('dj.life', 'r') as file:
    dj_life = json.load(file)

print(dj_life)

with open('config.json', 'r') as file:
    config = json.load(file)

print(config)

with open('config.json', 'w') as file:
    json.dump(config, file, indent=2)
