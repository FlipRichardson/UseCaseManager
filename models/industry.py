from sqlalchemy import Column, Integer, String
from models.base import Base

class Industry(Base):
    """
    Industry table for a company and use case.
    
    Attributes:
        id (int): Primary key identifier for the industry.
        name (str): Name of the industry (max 100 characters, unique).
    """
    __tablename__ = 'industries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Industry(id={self.id}, name='{self.name}')>"