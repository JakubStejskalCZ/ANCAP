from sqlalchemy import Column, Integer, String, Float, Boolean
from base import Base

class PublicProject(Base):
    __tablename__ = "public_projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    funds_raised = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
