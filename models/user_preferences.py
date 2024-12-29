from sqlalchemy import Column, Integer, String
from models.base import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(Integer, unique=True, nullable=False)
    locale = Column(String, default="en", nullable=False)
