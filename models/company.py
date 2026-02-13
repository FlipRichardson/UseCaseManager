from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Company(Base):
    """
    Company table for company information.
    
    Attributes:
        id (int): Primary key identifier for the company.
        name (str): Name of the company (max 200 characters).
        industry_id (int): Foreign key reference to the industries table.
        industry (Industry): Relationship to the Industry model, providing access
            to the associated industry object.
    
    Relationships:
        - Many-to-One with Industry: Multiple companies can belong to one industry.
        - Backref 'companies' on Industry allows accessing all companies in an industry.
    """
    __tablename__ = 'companies'

    # attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)

    # connection to industry id (company.industry)
    industry = relationship("Industry", backref="companies")

    # repr - print
    def __repr__(self):
        return f"<Company(id = {self.id}, name = '{self.name}', industry_id = {self.industry_id})>"