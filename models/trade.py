from sqlalchemy import Column, Integer, Float, ForeignKey
from base import Base

class TradeRoute(Base):
    __tablename__ = "trade_routes"

    id = Column(Integer, primary_key=True)
    region_a_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    region_b_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    trade_volume = Column(Float, default=0.0)
    tariff_rate = Column(Float, default=0.0)
