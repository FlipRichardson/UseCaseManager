from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from models.base import Base

# helper - many to many relationship - use case id to person id
use_case_person = Table(
    'use_case_person',
    Base.metadata,
    Column('use_case_id', Integer, ForeignKey('use_cases.id'), primary_key=True),
    Column('person_id', Integer, ForeignKey('persons.id'), primary_key=True)
)


class UseCase(Base):
    """
    UseCase table for storing business use cases within companies.
    
    Attributes:
        id (int): Primary key identifier for the use case.
        title (str): Title of the use case (max 250 characters).
        description (str): Detailed description of the use case (optional).
        expected_benefit (str): Expected benefits from implementing the use case (optional).
        status (str): Current status of the use case (max 100 characters, defaults to 'new').
        company_id (int): Foreign key reference to the companies table.
        industry_id (int): Foreign key reference to the industries table.
        company (Company): Relationship to the Company model.
        industry (Industry): Relationship to the Industry model.
        persons (list[Person]): Many-to-Many relationship with Person model,
            representing people involved in the use case.
    
    Relationships:
        - Many-to-One with Company: Multiple use cases can belong to one company.
        - Many-to-One with Industry: Multiple use cases can belong to one industry.
        - Many-to-Many with Person: A use case can involve multiple persons,
          and a person can be involved in multiple use cases.
    """
    __tablename__ = 'use_cases'

    # attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    expected_benefit = Column(Text, nullable=True)
    status = Column(String(100), nullable=False, default='new')

    # connections
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    industry_id = Column(Integer, ForeignKey('industries.id'), nullable=False)

    # relationships
    company = relationship("Company", backref='use_cases')
    industry = relationship("Industry", backref='use_cases')
    persons = relationship("Person", secondary=use_case_person, backref='use_cases')

    def __repr__(self):
        return f"<UseCase(id={self.id}, title='{self.title}', status='{self.status}', company_id={self.company_id})>"