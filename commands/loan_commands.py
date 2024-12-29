from discord.ext import commands
from sqlalchemy import select
from models.loans import Loan
from models.citizen import Citizen
from utils.translator import Translator

class LoanCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def offer_loan(self, ctx, borrower_id: int, amount: float, interest_rate: float, repayment_term: int):
        """Offer a loan to another user."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate lender existence
            lender = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            lender = lender.scalars().first()
            if not lender:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Validate borrower existence
            borrower = await session.execute(select(Citizen).where(Citizen.id == borrower_id))
            borrower = borrower.scalars().first()
            if not borrower:
                message = self.translator.translate("borrower_not_found")
                await ctx.send(message)
                return

            # Check lender's balance
            if lender.balance < amount:
                message = self.translator.translate("insufficient_balance")
                await ctx.send(message)
                return

            # Create loan
            loan = Loan(
                lender_id=lender.id,
                borrower_id=borrower.id,
                amount=amount,
                interest_rate=interest_rate,
                repayment_term=repayment_term,
                remaining_balance=amount
            )
            session.add(loan)
            lender.balance -= amount  # Deduct amount from lender's balance
            borrower.balance += amount  # Add amount to borrower's balance
            await session.commit()

            # Notify lender
            message = self.translator.translate("loan_offered", amount=amount, borrower=borrower.name)
            await ctx.send(message)

    @commands.command()
    async def list_loans(self, ctx):
        """List all loans where the user is involved."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve loans
            loans = await session.execute(
                select(Loan).where((Loan.lender_id == citizen.id) | (Loan.borrower_id == citizen.id))
            )
            loans = loans.scalars().all()

            if not loans:
                message = self.translator.translate("no_loans_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- Loan ID: {loan.id} | Amount: {loan.amount} ancapy | Remaining: {loan.remaining_balance} ancapy | "
                    f"Interest: {loan.interest_rate}% | Borrower: {loan.borrower_id} | Lender: {loan.lender_id}"
                    for loan in loans
                ]
            )
            message = self.translator.translate("loan_list", loans=response)
            await ctx.send(message)

    @commands.command()
    async def repay_loan(self, ctx, loan_id: int, amount: float):
        """Repay a loan."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            borrower = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            borrower = borrower.scalars().first()
            if not borrower:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve loan
            loan = await session.get(Loan, loan_id)
            if not loan or loan.borrower_id != borrower.id:
                message = self.translator.translate("loan_not_found_or_not_borrower")
                await ctx.send(message)
                return

            # Validate repayment amount
            if amount > borrower.balance:
                message = self.translator.translate("insufficient_balance")
                await ctx.send(message)
                return
            if amount > loan.remaining_balance:
                message = self.translator.translate("overpayment", remaining=loan.remaining_balance)
                await ctx.send(message)
                return

            # Process repayment
            loan.remaining_balance -= amount
            borrower.balance -= amount
            lender = await session.get(Citizen, loan.lender_id)
            lender.balance += amount
            await session.commit()

            # Notify borrower
            message = self.translator.translate("loan_repaid", amount=amount, remaining=loan.remaining_balance)
            await ctx.send(message)
