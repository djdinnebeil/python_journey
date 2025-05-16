from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, Session
import os

# === SQLAlchemy ORM Setup (2.0 Style) ===
Base = declarative_base()

# Association tables
db_path = "social_network.db"

friendships = Table(
    'friendships', Base.metadata,
    Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('people.id'), primary_key=True)
)

club_members = Table(
    'club_members', Base.metadata,
    Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('club_id', Integer, ForeignKey('clubs.id'), primary_key=True)
)

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    friends = relationship("Person",
                           secondary=friendships,
                           primaryjoin=id == friendships.c.person_id,
                           secondaryjoin=id == friendships.c.friend_id)
    clubs = relationship("Club", secondary=club_members, back_populates="members")

class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    members = relationship("Person", secondary=club_members, back_populates="clubs")

def create_database(db_path="social_network.db"):
    """
    Creates the database and returns an SQLAlchemy engine and models.
    """
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
    Base.metadata.create_all(engine)
    return engine, Club, Person, friendships, club_members

engine, Club, Person, friendships, club_members = create_database()

session = Session(engine)