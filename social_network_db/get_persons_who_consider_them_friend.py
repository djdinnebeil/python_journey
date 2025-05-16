from db_social_refactored import session, Club, Person, friendships, club_members
from sqlalchemy import select
from seed_optimized import load_data_from_csv

# GRADED CELL 4 - Do NOT delete it, do NOT place your solution anywhere else. You can create new cells and work from there, but in the end add your solution in this cell.
def get_persons_who_consider_them_friend(session, person_name):
    """
    Returns a list of Person objects who consider the specified person as their friend,
    in a scenario where friendships are unidirectional.

    Parameters:
    - person_name (str): The name of the person to find who is considered as a friend by others.

    Returns:
    - List[Person]: A list of Person objects who consider the specified person as their friend.
    """
    ### START CODE HERE ###
    stmt = select(Person).where(Person.name == person_name)
    person = session.execute(stmt).scalar_one_or_none()

    if not person:
        return []

    stmt = select(Person).join(friendships, Person.id == friendships.c.person_id).where(
        friendships.c.friend_id == person.id)
    return session.execute(stmt).scalars().all()

# Example usage of the get_persons_who_consider_them_friend function
load_data_from_csv(session, Club, Person, friendships, club_members, "members.csv")

# Fetching people who consider given name as their friend
name = 'John Rocha'

name_friend_of = get_persons_who_consider_them_friend(session, name)

# Printing out the names of all people who consider Alice as their friend
print(f"People who consider {name} as their friend:")
for person in name_friend_of:
    print(f"- {person.name}, Age: {person.age}, Location: {person.location}")