from discord.ext import commands
from sqlalchemy import select
from models.citizen import Citizen
from notifications.base import NotificationBase
from utils.translator import Translator

class CitizenCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_citizen(self, ctx, name: str = None, nickname: str = None):
        """Create a new citizen in the simulation."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Check if the user already exists
            existing_citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            if existing_citizen.scalars().first():
                message = self.translator.translate("citizen_exists")
                await ctx.send(message)
                return

            # Generate default values if not provided
            name = name or f"Citizen_{user_id}"
            nickname = nickname or f"Player_{user_id}"
            starting_balance = 1000.0  # Default starting balance

            # Create the citizen
            citizen = Citizen(
                discord_id=user_id,
                name=name,
                nickname=nickname,
                balance=starting_balance
            )
            session.add(citizen)
            await session.commit()

            # Notify user
            success_message = self.translator.translate("citizen_created", name=name, balance=starting_balance)
            await ctx.send(success_message)

    @commands.command()
    async def get_citizen(self, ctx):
        """Get information about your citizen."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve citizen
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()

            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Prepare citizen details
            details = self.translator.translate(
                "citizen_details",
                name=citizen.name,
                nickname=citizen.nickname or "N/A",
                balance=citizen.balance
            )
            await ctx.send(details)

    @commands.command()
    async def delete_citizen(self, ctx):
        """Delete your citizen from the simulation."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve and delete citizen
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()

            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            await session.delete(citizen)
            await session.commit()

            # Notify user
            message = self.translator.translate("citizen_deleted", name=citizen.name)
            await ctx.send(message)
