import requests
import json

with open('config.json', 'r') as file:
    config = json.load(file)

# Sending a GET request
response = requests.get('http://127.0.0.1:5000/greet', params={'name': 'DJ'})
print('GET Response:', response.json())

# Sending a POST request
data = config
response = requests.post('http://127.0.0.1:5000/data', json=data)
print('POST Response:', response.json())
