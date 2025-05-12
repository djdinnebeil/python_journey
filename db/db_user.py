from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_tables import User

engine = create_engine('sqlite:///ecommerce.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def add_user(name, email):
    """
    Adds a new user to the database.

    Args:
        name (str): The name of the user.
        email (str): The email of the user.

    Returns:
        str: Success or error message.
    """
    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        return 'User \'{name}\' added successfully!'
    except Exception as e:
        session.rollback()
        return f'Error occurred: {e}'
    finally:
        session.close()

def get_user_by_id(user_id):
    """
    Retrieves a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: User information or an error message.
    """
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return f'User found: ID={user.id}, Name={user.name}, Email={user.email}'
        else:
            return f'No user found with ID={user_id}'
    except Exception as e:
        return f'Error occurred: {e}'

def get_all_users():
    """
    Retrieves all users from the database.

    Returns:
        list: A list of user dictionaries.
    """
    try:
        users = session.query(User).all()
        if users:
            return [f'ID={user.id}, Name={user.name}, Email={user.email}' for user in users]
        else:
            return 'No users found.'
    except Exception as e:
        return f'Error occurred: {e}'

# name = input('Name')
# email = input('Email')
# add_user(name, email)

print(get_user_by_id(2))
print(get_all_users())