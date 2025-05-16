# The members.csv file contains 20 people. The code below will show you the first 5 rows to help you understand the format of the CSV file
from db_social import create_database
import pandas as pd

pd.read_csv("members.csv", converters = {'Friendships': eval, "Clubs": eval}).head()

def load_data_from_csv(session, Club, Person, friendships, club_members, csv_path="members.csv"):
    """
    Load data from a CSV file into the database, clearing existing data and creating new records for people, clubs, friendships, and club memberships.

    This function performs several key operations:
    1. Clears existing data from the Person, Club, friendships, and club_members tables.
    2. Reads data from a CSV file specified by `csv_path`, defaulting to "members.csv".
    3. For each row in the CSV, it creates or retrieves clubs mentioned, creates a person with the specified attributes, and associates them with the clubs.
    4. Establishes friendships based on the "Friendships" column in the CSV, which lists friend IDs for each person.
    5. Commits all changes to the database to ensure data integrity and consistency.

    Parameters:
    - session: The SQLAlchemy session object used for database transactions.
    - Club: The Club class model used to create or retrieve club records.
    - Person: The Person class model used to create person records.
    - friendships: The table/model representing friendships between people.
    - club_members: The table/model representing memberships of people in clubs.
    - csv_path (str, optional): The path to the CSV file containing the data to be loaded. Defaults to "members.csv".

    Returns:
    None. The function operates by side effects, modifying the database directly.

    Note:
    The function assumes the CSV file is formatted with specific columns: "ID", "Name", "Surname", "Age", "Gender", "Location", "Clubs", and "Friendships".
    "Clubs" is expected to be string representations of lists and "Friendships" is expected to be a list of IDs representing the member friends.
    """
    # Step 1: Clear existing data from all relevant tables
    session.query(Person).delete()
    session.query(Club).delete()
    session.query(friendships).delete()
    session.query(club_members).delete()

    session.commit()  # Commit the deletion of all existing records

    # Load the CSV data
    df = pd.read_csv("members.csv", converters = {'Friendships': eval, "Clubs": eval})
    ### START CODE HERE ###

    # Dictionary to cache Club and Person objects by ID
    club_lookup = {}
    person_lookup = {}

    # Step 1: Create all Person and Club objects
    for _, row in df.iterrows():
        # Create or get Club objects
        person_clubs = []
        for club_desc in row['Clubs']:
            if club_desc not in club_lookup:
                club = Club(description=club_desc)
                session.add(club)
                club_lookup[club_desc] = club
            person_clubs.append(club_lookup[club_desc])

        # Create Person object
        person = Person(
            id=row['ID'],
            name=f"{row['Name']} {row['Surname']}",
            age=row['Age'],
            gender=row['Gender'],
            location=row['Location'],
            clubs=person_clubs
        )
        session.add(person)
        person_lookup[row['ID']] = person

    session.commit()  # Commit early so IDs are established

    # Step 2: Establish friendships
    for _, row in df.iterrows():
        person = person_lookup[row['ID']]
        for friend_id in row['Friendships']:
            if friend_id in person_lookup:
                friend = person_lookup[friend_id]
                # Avoid duplicates: only add if not already friends
                if friend not in person.friends:
                    person.friends.append(friend)

    session.commit()

# The code below creates the database and reads in the data
session, Club, Person, friendships, club_members = create_database()
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