from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from base import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    rent_fee = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True)
