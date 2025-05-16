from db_social_refactored import session, Club, Person, friendships, club_members
import pandas as pd

def load_data_from_csv(session, Club, Person, friendships, club_members, csv_path="members.csv"):
    """
    Load people, clubs, and friendships from a CSV into the database.

    This optimized version improves performance using:
    - Bulk inserts for clubs and people
    - Tuple-based row iteration
    - Set-based friendship deduplication
    - One transaction for everything

    Parameters:
        session: SQLAlchemy session for DB operations
        Club, Person: SQLAlchemy ORM models
        friendships, club_members: association tables (not directly used here)
        csv_path (str): Path to CSV file (default "members.csv")

    Returns:
        None
    """

    # Step 1: Clear all existing records from tables
    session.query(Person).delete()
    session.query(Club).delete()
    session.query(friendships).delete()
    session.query(club_members).delete()
    session.commit()

    # Step 2: Load the CSV data and convert stringified lists into actual Python lists
    import pandas as pd
    df = pd.read_csv(csv_path, converters={'Friendships': eval, 'Clubs': eval})

    # Step 3: Create all unique clubs first, avoiding duplicates
    unique_club_names = set(club_name for clubs in df['Clubs'] for club_name in clubs)
    club_lookup = {desc: Club(description=desc) for desc in unique_club_names}

    # Bulk insert all Club objects at once (faster than individual inserts)
    session.add_all(club_lookup.values())

    # Step 4: Create all Person objects and link them to Club objects
    person_lookup = {}
    people_to_insert = []

    for row in df.itertuples(index=False):
        row: any
        full_name = f"{row.Name} {row.Surname}"
        person = Person(
            id=row.ID,
            name=full_name,
            age=row.Age,
            gender=row.Gender,
            location=row.Location,
            clubs=[club_lookup[desc] for desc in row.Clubs]  # many-to-many club links
        )
        person_lookup[row.ID] = person
        people_to_insert.append(person)

    # Bulk insert all Person objects
    session.add_all(people_to_insert)

    # Step 5: Now establish friendships (self-referencing many-to-many)
    for row in df.itertuples(index=False):
        row: any
        person = person_lookup[row.ID]
        added_friends = set()
        for friend_id in row.Friendships:
            # Only add if friend exists and hasn't already been linked
            if friend_id in person_lookup and friend_id not in added_friends:
                person.friends.append(person_lookup[friend_id])
                added_friends.add(friend_id)

    # Step 6: Commit everything to the database
    session.commit()

# The code below creates the database and reads in the data
# load_data_from_csv(session, Club, Person, friendships, club_members, "members.csv")

if __name__ == '__main__':
    load_data_from_csv(session, Club, Person, friendships, club_members, "members.csv")

    # If your load_data_from_csv function is working correctly, then you should have read in data correctly into all four tables in the database.
    print_amount = 3

    # Print first 3 persons
    print("=== All Persons ===")
    people = session.query(Person).all()
    for person in people[:print_amount ]:
        print(f"ID: {person.id}, Name: {person.name}, Age: {person.age}, Gender: {person.gender}, Location: {person.location}")

    # Print first 3 clubs and their members
    print("\n=== All Clubs and their Members ===")
    clubs = session.query(Club).all()
    for club in clubs[:print_amount ]:
        print(f"Club ID: {club.id}, Description: {club.description}, Members: {[member.name for member in club.members]}")

    # Print friendships of first three persons
    print("\n=== Friendships ===")
    for person in people[:print_amount ]:
        friends = [friend.name for friend in person.friends]
        print(f"{person.name}'s Friends: {friends}")