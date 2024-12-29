from discord.ext import commands
from sqlalchemy import select
from models.region import Region
from models.citizen import Citizen
from utils.translator import Translator
from notifications.prosperity_change import ProsperityChangeNotification

class RegionCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_region(self, ctx, name: str):
        """Create a new region."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Create region
            region = Region(
                name=name,
                owner_id=citizen.id,
                prosperity=50.0,  # Default prosperity
                pollution=0.0  # Default pollution level
            )
            session.add(region)
            await session.commit()

            # Notify user
            message = self.translator.translate("region_created", name=name)
            await ctx.send(message)

    @commands.command()
    async def list_regions(self, ctx):
        """List all regions."""
        async with self.session() as session:
            regions = await session.execute(select(Region))
            regions = regions.scalars().all()

            if not regions:
                message = self.translator.translate("no_regions_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- {region.name} | Prosperity: {region.prosperity:.2f} | Pollution: {region.pollution:.2f}"
                    for region in regions
                ]
            )
            message = self.translator.translate("region_list", regions=response)
            await ctx.send(message)

    @commands.command()
    async def update_prosperity(self, ctx, region_id: int, new_prosperity: float):
        """Update the prosperity of a region."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve region
            region = await session.get(Region, region_id)
            if not region:
                message = self.translator.translate("region_not_found")
                await ctx.send(message)
                return

            # Validate ownership
            if region.owner_id != user_id:
                message = self.translator.translate("not_region_owner")
                await ctx.send(message)
                return

            # Update prosperity
            old_prosperity = region.prosperity
            region.prosperity = max(0, new_prosperity)  # Ensure prosperity is non-negative
            await session.commit()

            # Send prosperity change notification
            notification = ProsperityChangeNotification(
                guild=ctx.guild,
                region_name=region.name,
                old_prosperity=old_prosperity,
                new_prosperity=region.prosperity
            )
            await notification.send()

            # Notify user
            message = self.translator.translate(
                "region_prosperity_updated",
                name=region.name,
                old=old_prosperity,
                new=region.prosperity
            )
            await ctx.send(message)

    @commands.command()
    async def update_pollution(self, ctx, region_id: int, new_pollution: float):
        """Update the pollution level of a region."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve region
            region = await session.get(Region, region_id)
            if not region:
                message = self.translator.translate("region_not_found")
                await ctx.send(message)
                return

            # Validate ownership
            if region.owner_id != user_id:
                message = self.translator.translate("not_region_owner")
                await ctx.send(message)
                return

            # Update pollution
            old_pollution = region.pollution
            region.pollution = max(0, new_pollution)  # Ensure pollution is non-negative
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "region_pollution_updated",
                name=region.name,
                old=old_pollution,
                new=region.pollution
            )
            await ctx.send(message)
