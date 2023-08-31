# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLite database engine
engine = create_engine('sqlite:///many_to_many.db')

# Create a base class for declarative models
Base = declarative_base()

# Define a class representing the "Game" table
class Game(Base):
    # Table name
    __tablename__ = 'games'

    # Columns of the table
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Define a one-to-many relationship between Game and Review
    reviews = relationship('Review', back_populates='game', cascade='all, delete-orphan')
    
    # Define an association proxy to access users through reviews
    users = association_proxy('reviews', 'user',
        creator=lambda us: Review(user=us))

    # Define a string representation for the Game class
    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

# Define a class representing the "User" table
class User(Base):
    # Table name
    __tablename__ = 'users'

    # Columns of the table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Define a one-to-many relationship between User and Review
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    # Define an association proxy to access games through reviews
    games = association_proxy('reviews', 'game',
        creator=lambda gm: Review(game=gm))

    # Define a string representation for the User class
    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name})'

# Define a class representing the "Review" table
class Review(Base):
    # Table name
    __tablename__ = 'reviews'

    # Columns of the table
    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Define foreign key relationships to Game and User
    game_id = Column(Integer(), ForeignKey('games.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    # Define relationships between Review and Game/User
    game = relationship('Game', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    # Define a string representation for the Review class
    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'
