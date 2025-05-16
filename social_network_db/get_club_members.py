from db_social_refactored import session, Club, Person, friendships, club_members
from sqlalchemy import select
from seed_optimized import load_data_from_csv

# GRADED CELL 2 - Do NOT delete it, do NOT place your solution anywhere else. You can create new cells and work from there, but in the end add your solution in this cell.
def get_club_members(session, club_description):
    """
    Returns a list of Person objects who are members of a club given the club's description.

    Parameters:
    - session: The SQLAlchemy session for database queries.
    - club_description (str): The description of the club for which members are to be retrieved.

    Returns:
    - List[Person]: A list of Person objects who are members of the specified club.
    """
    ### START CODE HERE ###
    stmt = (
        select(Club)
        .where(Club.description == club_description)
        .limit(1)
    )
    club_result = session.execute(stmt).scalar_one_or_none()

    if club_result:
        return club_result.members
    return []

# Example usage of the get_club_members function

# Assume the session and all models have been correctly set up and populated as per your initial code
load_data_from_csv(session, Club, Person, friendships, club_members, "members.csv")

# Fetching members of the "Hiking Club"
hiking_club_members = get_club_members(session, "Hiking Club")

# Printing out the names of all members of the Hiking Club
print("Members of the Hiking Club:")
for person in hiking_club_members:
    print(f"- {person.name}, Age: {person.age}, Location: {person.location}")