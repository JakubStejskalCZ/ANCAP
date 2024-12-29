from sqlalchemy import Column, Integer, String, Float, ForeignKey
from base import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)
    prosperity = Column(Float, default=50.0)
    pollution = Column(Float, default=0.0)
