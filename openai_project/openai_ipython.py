from openai import OpenAI
import os
import dotenv
from IPython.display import display, Markdown


dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

models = client.models.list()
print([m.id for m in models])

YOUR_PROMPT = "What is the difference between happiness and joy?"

client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role" : "user", "content" : YOUR_PROMPT}]
)

def get_response(client: OpenAI, messages: str, model: str = "gpt-4.1-nano") -> str:
    return client.chat.completions.create(
        model=model,
        messages=messages
    )

def system_prompt(message: str) -> dict:
    return {"role": "developer", "content": message}

def assistant_prompt(message: str) -> dict:
    return {"role": "assistant", "content": message}

def user_prompt(message: str) -> dict:
    return {"role": "user", "content": message}

def pretty_print(message: str) -> str:
    print(message.choices[0].message.content)

messages = [user_prompt(YOUR_PROMPT)]

chatgpt_response = get_response(client, messages)

pretty_print(chatgpt_response)