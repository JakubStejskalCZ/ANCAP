from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import enum

class CompanyType(enum.Enum):
    INSURANCE = "insurance"
    SERVICES = "services"
    OTHER = "other"

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    balance = Column(Float, default=0.0)
    company_type = Column(Enum(CompanyType), nullable=False)

    # Insurance
    provides_insurance = Column(Boolean, default=False)
    insurance_offers = relationship("InsuranceOffer", back_populates="company")
