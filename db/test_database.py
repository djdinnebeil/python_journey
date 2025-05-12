import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_tables import Base, User
from db_user import add_user, get_user_by_id, get_all_users

# Use an in-memory SQLite database for testing
@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# def test_add_user(test_session):
#     result = add_user('Test User', 'test@example.com')
#     assert 'added successfully' in result

def test_get_user_by_id(test_session):
    # Add a user to test retrieval
    add_user('DJ', 'djdinn11@gmail.com')
    result = get_user_by_id(1)
    assert 'User found' in result
    assert 'Name=DJ in result'

def test_get_user_by_id_not_found(test_session):
    result = get_user_by_id(999)
    assert 'No user found' in result

def test_get_all_users(test_session):
    # Add multiple users
    add_user('DJ', 'alice@example.com')
    add_user('Daniel', 'bob@example.com')
    result = get_all_users()
    assert len(result) >= 2
    assert any('Name=DJ' in user for user in result)
    assert any('Name=Daniel' in user for user in result)
