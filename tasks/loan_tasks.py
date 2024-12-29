from sqlalchemy import select
from models.loans import Loan
from models.citizen import Citizen
from utils.translator import Translator
from notifications.failed_loan_payment import FailedLoanPaymentNotification

async def process_loan_repayments(session, guild):
    """
    Process monthly loan repayments for all borrowers.
    Deduct repayments from their balances and update loan balances.
    Handle missed payments by notifying lenders.
    """
    async with session() as session:
        loans = await session.execute(
            select(Loan).where(Loan.remaining_balance > 0)
        )
        loans = loans.scalars().all()

        for loan in loans:
            # Retrieve borrower and lender
            borrower = await session.get(Citizen, loan.borrower_id)
            lender = await session.get(Citizen, loan.lender_id)

            if not borrower or not lender:
                continue  # Skip invalid or missing data

            # Calculate monthly repayment amount
            monthly_payment = loan.amount / loan.repayment_term
            monthly_payment_with_interest = monthly_payment + (loan.interest_rate / 100 * loan.remaining_balance)

            # Check if borrower has enough balance
            if borrower.balance >= monthly_payment_with_interest:
                # Deduct repayment and transfer to lender
                borrower.balance -= monthly_payment_with_interest
                lender.balance += monthly_payment_with_interest
                loan.remaining_balance -= monthly_payment
            else:
                # Handle missed payment
                notification = FailedLoanPaymentNotification(
                    guild=guild,
                    borrower_name=borrower.name,
                    lender_name=lender.name,
                    loan_id=loan.id
                )
                await notification.send()

        await session.commit()
