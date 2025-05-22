from openai import OpenAI
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models = client.models.list()
print([m.id for m in models])
