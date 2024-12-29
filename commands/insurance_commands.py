from discord.ext import commands
from sqlalchemy import select
from models.citizen import Citizen
from models.company import Company
from models.insurance_offer import InsuranceOffer, InsuranceOfferStatus
from utils.translator import Translator
from notifications.insurance_request import InsuranceRequestNotification

class InsuranceCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def request_insurance(self, ctx, company_id: int):
        """Request insurance from a company."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Validate company existence and insurance offering
            company = await session.get(Company, company_id)
            if not company or not company.provides_insurance:
                message = self.translator.translate("company_not_insurance")
                await ctx.send(message)
                return

            # Create an insurance offer
            offer = InsuranceOffer(
                citizen_id=citizen.id,
                company_id=company.id,
                status=InsuranceOfferStatus.PENDING
            )
            session.add(offer)
            await session.commit()

            # Notify company owner
            notification = InsuranceRequestNotification(
                guild=ctx.guild,
                citizen_name=citizen.name,
                company_name=company.name,
                owner_discord_id=company.owner_id
            )
            await notification.send()

            # Notify user
            message = self.translator.translate("insurance_request_sent", company_name=company.name)
            await ctx.send(message)

    @commands.command()
    async def list_insurance_offers(self, ctx):
        """List all insurance offers for the user."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve offers
            offers = await session.execute(select(InsuranceOffer).where(InsuranceOffer.citizen_id == citizen.id))
            offers = offers.scalars().all()

            if not offers:
                message = self.translator.translate("no_insurance_offers")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- Offer ID: {offer.id} | Company: {offer.company.name} | Status: {offer.status.value}"
                    for offer in offers
                ]
            )
            message = self.translator.translate("insurance_offers_list", offers=response)
            await ctx.send(message)

    @commands.command()
    async def respond_insurance_request(self, ctx, offer_id: int, action: str, monthly_fee: float = None):
        """Respond to an insurance request as a company owner."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve offer
            offer = await session.get(InsuranceOffer, offer_id)
            if not offer:
                message = self.translator.translate("insurance_offer_not_found")
                await ctx.send(message)
                return

            # Validate ownership
            company = await session.get(Company, offer.company_id)
            if not company or company.owner_id != user_id:
                message = self.translator.translate("not_company_owner")
                await ctx.send(message)
                return

            # Process response
            if action.lower() == "accept":
                if not monthly_fee:
                    message = self.translator.translate("fee_required")
                    await ctx.send(message)
                    return
                offer.status = InsuranceOfferStatus.ACCEPTED
                offer.monthly_fee = monthly_fee
                message = self.translator.translate("insurance_offer_accepted", fee=monthly_fee)
            elif action.lower() == "reject":
                offer.status = InsuranceOfferStatus.REJECTED
                message = self.translator.translate("insurance_offer_rejected")
            else:
                message = self.translator.translate("invalid_action")
                await ctx.send(message)
                return

            await session.commit()
            await ctx.send(message)

    @commands.command()
    async def confirm_insurance(self, ctx, offer_id: int):
        """Confirm an insurance offer and switch from state insurance."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve offer
            offer = await session.get(InsuranceOffer, offer_id)
            if not offer or offer.status != InsuranceOfferStatus.ACCEPTED:
                message = self.translator.translate("insurance_offer_invalid")
                await ctx.send(message)
                return

            # Confirm insurance
            citizen.insurance_company_id = offer.company_id
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "insurance_confirmed", company_name=offer.company.name, fee=offer.monthly_fee
            )
            await ctx.send(message)
