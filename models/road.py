from sqlalchemy import Column, Integer, String, Float, ForeignKey
from base import Base

class Road(Base):
    __tablename__ = "roads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    access_fee = Column(Float, nullable=False)
