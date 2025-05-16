class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # One-to-one: uselist=False makes it a scalar, not a list
    profile = relationship('Profile', back_populates='user', uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)  # Enforce one-to-one

    user = relationship('User', back_populates='profile')