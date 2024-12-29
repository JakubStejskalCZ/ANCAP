from discord.ext import commands
from sqlalchemy import select
from models.trade import TradeRoute
from models.region import Region
from utils.translator import Translator

class TradeCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_trade_route(self, ctx, region_a_id: int, region_b_id: int, tariff_rate: float):
        """Create a new trade route between two regions."""
        async with self.session() as session:
            # Validate regions
            region_a = await session.get(Region, region_a_id)
            region_b = await session.get(Region, region_b_id)

            if not region_a or not region_b:
                message = self.translator.translate("region_not_found")
                await ctx.send(message)
                return

            # Check if trade route already exists
            existing_route = await session.execute(
                select(TradeRoute).where(
                    (TradeRoute.region_a_id == region_a_id) & (TradeRoute.region_b_id == region_b_id)
                )
            )
            if existing_route.scalars().first():
                message = self.translator.translate("trade_route_exists")
                await ctx.send(message)
                return

            # Create trade route
            trade_route = TradeRoute(
                region_a_id=region_a_id,
                region_b_id=region_b_id,
                tariff_rate=tariff_rate
            )
            session.add(trade_route)
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "trade_route_created",
                region_a=region_a.name,
                region_b=region_b.name,
                tariff_rate=tariff_rate
            )
            await ctx.send(message)

    @commands.command()
    async def list_trade_routes(self, ctx):
        """List all trade routes."""
        async with self.session() as session:
            routes = await session.execute(select(TradeRoute))
            routes = routes.scalars().all()

            if not routes:
                message = self.translator.translate("no_trade_routes_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- {route.region_a.name} <-> {route.region_b.name} | Tariff Rate: {route.tariff_rate:.2f}%"
                    for route in routes
                ]
            )
            message = self.translator.translate("trade_route_list", routes=response)
            await ctx.send(message)

    @commands.command()
    async def update_tariff_rate(self, ctx, trade_route_id: int, new_rate: float):
        """Update the tariff rate for a trade route."""
        async with self.session() as session:
            # Retrieve trade route
            trade_route = await session.get(TradeRoute, trade_route_id)
            if not trade_route:
                message = self.translator.translate("trade_route_not_found")
                await ctx.send(message)
                return

            # Update tariff rate
            old_rate = trade_route.tariff_rate
            trade_route.tariff_rate = new_rate
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "trade_route_tariff_updated",
                region_a=trade_route.region_a.name,
                region_b=trade_route.region_b.name,
                old=old_rate,
                new=new_rate
            )
            await ctx.send(message)

    @commands.command()
    async def delete_trade_route(self, ctx, trade_route_id: int):
        """Delete an existing trade route."""
        async with self.session() as session:
            # Retrieve trade route
            trade_route = await session.get(TradeRoute, trade_route_id)
            if not trade_route:
                message = self.translator.translate("trade_route_not_found")
                await ctx.send(message)
                return

            # Delete trade route
            session.delete(trade_route)
            await session.commit()

            # Notify user
            message = self.translator.translate(
                "trade_route_deleted",
                region_a=trade_route.region_a.name,
                region_b=trade_route.region_b.name
            )
            await ctx.send(message)
