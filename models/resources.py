from sqlalchemy import Column, Integer, String, Float, ForeignKey
from base import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    extraction_rate = Column(Float, nullable=False)
