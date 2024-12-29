from discord.ext import commands
from sqlalchemy import select
from models.road import Road
from models.citizen import Citizen
from utils.translator import Translator

class RoadCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_road(self, ctx, name: str, access_fee: float):
        """Create a new road."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Create the road
            road = Road(
                name=name,
                owner_id=citizen.id,
                access_fee=access_fee,
                is_active=True
            )
            session.add(road)
            await session.commit()

            # Notify user
            message = self.translator.translate("road_created", name=name, access_fee=access_fee)
            await ctx.send(message)

    @commands.command()
    async def list_roads(self, ctx):
        """List all roads."""
        async with self.session() as session:
            roads = await session.execute(select(Road))
            roads = roads.scalars().all()

            if not roads:
                message = self.translator.translate("no_roads_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- {road.name} | Access Fee: {road.access_fee:.2f} ancapy | Status: {'Active' if road.is_active else 'Inactive'}"
                    for road in roads
                ]
            )
            message = self.translator.translate("road_list", roads=response)
            await ctx.send(message)

    @commands.command()
    async def update_access_fee(self, ctx, road_id: int, new_fee: float):
        """Update the access fee for a road."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve road
            road = await session.get(Road, road_id)
            if not road:
                message = self.translator.translate("road_not_found")
                await ctx.send(message)
                return

            # Validate ownership
            if road.owner_id != user_id:
                message = self.translator.translate("not_road_owner")
                await ctx.send(message)
                return

            # Update access fee
            old_fee = road.access_fee
            road.access_fee = new_fee
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "road_fee_updated", name=road.name, old=old_fee, new=new_fee
            )
            await ctx.send(message)

    @commands.command()
    async def deactivate_road(self, ctx, road_id: int):
        """Deactivate a road."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Retrieve road
            road = await session.get(Road, road_id)
            if not road:
                message = self.translator.translate("road_not_found")
                await ctx.send(message)
                return

            # Validate ownership
            if road.owner_id != user_id:
                message = self.translator.translate("not_road_owner")
                await ctx.send(message)
                return

            # Deactivate road
            road.is_active = False
            await session.commit()

            # Notify user
            message = self.translator.translate("road_deactivated", name=road.name)
            await ctx.send(message)
