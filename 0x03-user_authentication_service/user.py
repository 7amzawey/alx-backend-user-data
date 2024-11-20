#!/usr/bin/env python3
"""Create an SQLAlchemy module named User for a db table named users."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """Crearte a class user for a db table named user."""
    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullabel=False)
    session = Column(String, nullable=True)
    reset_token = Column(String, nullabe=True)
