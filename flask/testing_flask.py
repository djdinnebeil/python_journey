import requests

base_url = 'http://127.0.0.1:5000/api/greet'

# 1. Normal case
r = requests.get(f'{base_url}/DJ')
print(r.status_code, r.json())

# 2. Special characters (space)
r = requests.get(f'{base_url}/DJ%20Dinnebeil')
print(r.status_code, r.json())

# 3. Numbers
r = requests.get(f'{base_url}/12345')
print(r.status_code, r.json())

# 4. Missing name
r = requests.get(f'{base_url}/')
print(r.status_code)

# 5. Wrong method
r = requests.post(f'{base_url}/DJ')
if 'application/json' in r.headers.get('Content-Type', ''):
    print(r.status_code, r.json())
else:
    print(r.status_code, r.text)

# 5. Wrong method
r = requests.delete(f'{base_url}/DJ')
print(r.status_code, r.text)

# 6. Non-ASCII
r = requests.get(f'{base_url}/Álvaro')
print(r.status_code, r.json())

# 7. Very long name
r = requests.get(f'{base_url}/' + 'a' * 101)
print(r.status_code, r.text)

# 8. Invalid endpoint
r = requests.get('http://127.0.0.1:5000/api/unknownroute')
print(r.status_code)

# 4. Missing name (404)
r = requests.get(f'{base_url}/')
print(r.status_code, r.json())

# 5. Wrong method (405)
r = requests.delete(f'{base_url}/DJ')
print(r.status_code, r.json())

# 8. Invalid endpoint (404)
r = requests.get('http://127.0.0.1:5000/api/unknownroute')
print(r.status_code, r.json())

# 9. Invalid characters)
r = requests.get('http://127.0.0.1:5000/api/greet/<script>')
print(r.status_code, r.json())
