from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Company(Base):
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