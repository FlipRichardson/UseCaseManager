from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Person(Base):
    """
    Person table for storing individual person information within companies.
    
    Attributes:
        id (int): Primary key identifier for the person.
        name (str): Name of the person (max 200 characters).
        role (str): Role or job title of the person within the company (max 50 characters).
        company_id (int): Foreign key reference to the companies table.
        company (Company): Relationship to the Company model, providing access
            to the associated company object.
    
    Relationships:
        - Many-to-One with Company: Multiple persons can belong to one company.
        - Uses backref with 'persons' attribute on Company model.
    """
    __tablename__ = 'persons'

    # attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)  # may be ommitted
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    # relationships
    company = relationship("Company", backref="persons")

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', role='{self.role}')>"