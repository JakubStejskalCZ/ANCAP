from sqlalchemy import select
from models.insurance_offer import InsuranceOffer, InsuranceOfferStatus
from models.citizen import Citizen
from notifications.failed_insurance_payment import FailedInsurancePaymentNotification

async def process_insurance_payments(session, guild):
    """
    Process monthly insurance payments for all insured citizens.
    Deduct fees from their balances and handle failed payments.
    """
    async with session() as session:
        offers = await session.execute(
            select(InsuranceOffer).where(InsuranceOffer.status == InsuranceOfferStatus.ACCEPTED)
        )
        offers = offers.scalars().all()

        for offer in offers:
            # Retrieve insured citizen and their insurance company
            citizen = await session.get(Citizen, offer.citizen_id)
            company = await session.get(Citizen, offer.company_id)

            if not citizen or not company:
                continue  # Skip invalid or missing data

            # Check if citizen has enough balance
            if citizen.balance >= offer.monthly_fee:
                # Deduct monthly fee and transfer to company
                citizen.balance -= offer.monthly_fee
                company.balance += offer.monthly_fee
            else:
                # Handle failed payment
                notification = FailedInsurancePaymentNotification(
                    guild=guild,
                    citizen_name=citizen.name,
                    company_name=company.name
                )
                await notification.send()

                # Mark insurance as inactive after failure
                offer.status = InsuranceOfferStatus.INACTIVE

        await session.commit()
