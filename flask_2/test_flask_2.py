import pytest
from flask_2 import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Security Testing Demo" in response.data

def test_add_user(client):
    payload = {"username": "dj", "password": "strongpass"}
    response = client.post('/user', json=payload)
    assert response.status_code == 201
    assert b"User added successfully" in response.data

def test_get_user(client):
    # First add a user
    client.post('/user', json={"username": "alice", "password": "pw"})
    response = client.get('/user/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == "alice"
    assert 'password' not in data  # Confirm password is not exposed

def test_get_all_users(client):
    # First add a user
    client.post('/user', json={"username": "dj", "password": "admin6"})
    client.post('/user', json={"username": "daniel", "password": "admin6"})
    client.post('/user', json={"username": "jose", "password": "admin6"})
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['username'] == "dj"
    assert data[1]['username'] == "daniel"
    assert data[2]['username'] == "jose"
    assert 'password' not in data[0]  # Confirm password is not exposed

def test_update_user(client):
    client.post('/user', json={"username": "bob", "password": "123"})
    response = client.put('/user/1', json={"username": "bobby", "password": "456"})
    assert response.status_code == 200
    assert b"updated successfully" in response.data

def test_delete_user(client):
    client.post('/user', json={"username": "temp", "password": "delete"})
    response = client.delete('/user/1')
    assert response.status_code == 200
    assert b"deleted successfully" in response.data

def test_get_nonexistent_user(client):
    response = client.get('/user/999')
    assert response.status_code == 404
