"""
User model for authentication and authorization.
"""

from sqlalchemy import Column, Integer, String
from models.base import Base


class User(Base):
    """
    User table for authentication.
    
    Attributes:
        id (int): Primary key
        email (str): Email address (used for login, must be unique)
        password_hash (str): Hashed password (never store plain passwords!)
        role (str): User role - 'reader', 'maintainer', or 'admin'
        name (str): Optional display name
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"