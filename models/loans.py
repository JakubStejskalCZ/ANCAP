from sqlalchemy import Column, Integer, Float, ForeignKey
from base import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    lender_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    repayment_term = Column(Integer, nullable=False)
    remaining_balance = Column(Float, nullable=False)
