from sqlalchemy import Column, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import enum

class InsuranceOfferStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class InsuranceOffer(Base):
    __tablename__ = "insurance_offers"

    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    monthly_fee = Column(Float, nullable=True)
    status = Column(Enum(InsuranceOfferStatus), default=InsuranceOfferStatus.PENDING)

    # Relationships
    citizen = relationship("Citizen", back_populates="insurance_offers")
    company = relationship("Company", back_populates="insurance_offers")
