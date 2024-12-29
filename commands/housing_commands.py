from discord.ext import commands
from sqlalchemy import select
from models.housing import Property
from models.citizen import Citizen
from utils.translator import Translator

class HousingCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_property(self, ctx, address: str, rent_fee: float = None):
        """Create a new property."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Create the property
            property = Property(
                address=address,
                owner_id=citizen.id,
                rent_fee=rent_fee,
                is_available=True
            )
            session.add(property)
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "property_created",
                address=address,
                rent_fee=f"{rent_fee} ancapy/month" if rent_fee else "None"
            )
            await ctx.send(message)

    @commands.command()
    async def list_properties(self, ctx):
        """List all available properties."""
        async with self.session() as session:
            properties = await session.execute(select(Property).where(Property.is_available == True))
            properties = properties.scalars().all()

            if not properties:
                message = self.translator.translate("no_properties_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [f"- {property.address} (Rent: {property.rent_fee or 'N/A'} ancapy)" for property in properties]
            )
            message = self.translator.translate("property_list", properties=response)
            await ctx.send(message)

    @commands.command()
    async def rent_property(self, ctx, property_id: int):
        """Rent an available property."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve property
            property = await session.get(Property, property_id)
            if not property or not property.is_available:
                message = self.translator.translate("property_not_available")
                await ctx.send(message)
                return

            # Assign property to citizen
            property.is_available = False
            citizen.home_id = property.id
            await session.commit()

            # Notify user
            message = self.translator.translate("property_rented", address=property.address)
            await ctx.send(message)

    @commands.command()
    async def release_property(self, ctx):
        """Release your current property."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Validate current property
            if not citizen.home_id:
                message = self.translator.translate("no_property_rented")
                await ctx.send(message)
                return

            # Retrieve and release property
            property = await session.get(Property, citizen.home_id)
            property.is_available = True
            citizen.home_id = None
            await session.commit()

            # Notify user
            message = self.translator.translate("property_released", address=property.address)
            await ctx.send(message)
