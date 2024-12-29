from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    balance = Column(Float, default=1000.0)
    home_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    is_employed = Column(Boolean, default=False)
    insurance_company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    # Relationships
    insurance_offers = relationship("InsuranceOffer", back_populates="citizen")
