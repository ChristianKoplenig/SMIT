from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Auth(Base):
    """Schema for authentication module.

    Args:
        Base (declarative_base): SqlAlchemy Base Class
    """
    __tablename__ = 'auth'

    id = Column(Integer(), primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)

    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    sng_username = Column(String(100), nullable=False)
    sng_password = Column(String(100), nullable=False)
    daymeter = Column(String(100), nullable=False)
    nightmeter = Column(String(100), nullable=False)

def auth_table_setup() -> declarative_base:
    """Return constructor for auth table.

    Returns:
        declarative base: Base object for auth table
    """
    return Base