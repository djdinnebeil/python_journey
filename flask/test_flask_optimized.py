import requests

BASE_URL = 'http://127.0.0.1:5000/api/greet'

def request(method, endpoint):
    url = f'{BASE_URL}{endpoint}'
    if method == 'GET':
        return requests.get(url)
    elif method == 'POST':
        return requests.post(url)
    elif method == 'DELETE':
        return requests.delete(url)
    else:
        raise ValueError(f'Unsupported method: {method}')

# --- TEST CASES ---

def test_normal_case():
    r = request('GET', '/DJ')
    assert r.status_code == 200
    assert r.json()['message'] == 'Hello, DJ!'

def test_special_characters_space():
    r = request('GET', '/DJ%20Dinnebeil')
    assert r.status_code == 200
    assert r.json()['message'] == 'Hello, DJ Dinnebeil!'

def test_numbers():
    r = request('GET', '/12345')
    assert r.status_code == 200
    assert r.json()['message'] == 'Hello, 12345!'

def test_missing_name():
    r = request('GET', '/')
    assert r.status_code == 404

def test_method_post():
    r = request('POST', '/DJ')
    assert r.status_code == 200
    assert r.json()['message'] == 'This is POST by DJ.'

def test_wrong_method_delete():
    r = request('DELETE', '/DJ')
    assert r.status_code == 405
    assert r.json()['error'] == 'Method not allowed'

def test_non_ascii_name():
    r = request('GET', '/Álvaro')
    assert r.status_code == 200
    assert r.json()['message'] == 'Hello, Álvaro!'

def test_very_long_name():
    long_name = 'a' * 101
    r = request('GET', '/' + long_name)
    # Depending on your app logic, adjust expected behavior:
    assert r.status_code in (400, 200)

def test_invalid_endpoint():
    r = request('GET', '/api/unknownroute')
    assert r.status_code == 404

def test_invalid_characters():
    r = request('GET', '/<script>')
    assert r.status_code == 400 or r.status_code == 404  # Depending on Flask routing behavior
