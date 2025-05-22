import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv('api_key')
print(api_key)