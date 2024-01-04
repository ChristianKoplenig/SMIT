from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SomeUser(Base):
    """Schema for user table

    Args:
        Base (declarative_base): Base schema definition
    """
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now)