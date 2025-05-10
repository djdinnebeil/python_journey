import pickle
import io

# Explicitly hint the variable type to match the expected protocol
with open('dj.life', 'wb') as file: # type: io.IOBase
    pickle.dump({'dj': 'life423'}, file)

with open('dj.life', 'rb') as file:
    dj_life = pickle.load(file)

print(dj_life)

print(pickle.dumps(dj_life))