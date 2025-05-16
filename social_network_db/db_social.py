from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import numpy as np
import os
import json

# Creates the database for the social network

def create_database():
    Base = declarative_base()

    friendships = Table('friendships', Base.metadata,
                        Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
                        Column('friend_id', Integer, ForeignKey('people.id'), primary_key=True))

    club_members = Table('club_members', Base.metadata,
                         Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
                         Column('club_id', Integer, ForeignKey('clubs.id'), primary_key=True))

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

    if os.path.exists("social_network.db"):
        os.remove("social_network.db")
    engine = create_engine(f'sqlite:///{"social_network.db"}', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session, Club, Person, friendships, club_members

session, Club, Person, friendships, club_members = create_database()