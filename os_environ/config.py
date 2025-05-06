import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('KEY42', 'NOKEY42'))
