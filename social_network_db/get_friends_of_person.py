from db_social_refactored import session, Club, Person, friendships, club_members
from sqlalchemy import select
from seed_optimized import load_data_from_csv

# GRADED CELL 3 - Do NOT delete it, do NOT place your solution anywhere else. You can create new cells and work from there, but in the end add your solution in this cell.
def get_friends_of_person(session, person_name):
    """
    Returns a list of Person objects who are friends with the specified person.

    Parameters:
    - session: The SQLAlchemy session object used to query the database.
    - person_name (str): The name of the person for whom to retrieve friends.

    Returns:
    - List[Person]: A list of Person objects who are friends with the specified person.
    """
    ### START CODE HERE ###
    stmt = select(Person).where(Person.name == person_name)
    person = session.execute(stmt).scalar_one_or_none()

    if person:
        return person.friends
    return []

# Example usage of the get_friends_of_person function
load_data_from_csv(session, Club, Person, friendships, club_members, "members.csv")

# Fetching friends of given name
name = "John Rocha"

john_friends = get_friends_of_person(session, name)

# Printing out the names of all friends of John Rocha
print(f"Friends of {name}:")
for friend in john_friends:
    print(f"- {friend.name}, Age: {friend.age}, Location: {friend.location}")