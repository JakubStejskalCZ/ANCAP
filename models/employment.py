from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    employer_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    salary = Column(Float, nullable=False)
    terms = Column(String, nullable=False)
    is_open = Column(Boolean, default=True)
