import os
import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.base import Base
from utils.translator import Translator
from commands.citizen_commands import CitizenCommands
from commands.company_commands import CompanyCommands
from commands.region_commands import RegionCommands
from commands.road_commands import RoadCommands
from commands.housing_commands import HousingCommands
from commands.insurance_commands import InsuranceCommands
from commands.loan_commands import LoanCommands
from commands.trade_commands import TradeCommands
from commands.locale_commands import LocaleCommands
from commands.public_project_commands import PublicProjectCommands
from tasks.economy_tasks import update_region_economy
from tasks.insurance_tasks import process_insurance_payments
from tasks.loan_tasks import process_loan_repayments

# Bot configuration
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db")
PREFIX = "!"

# Translator locale setup (default is English)
LOCALE = os.getenv("LOCALE", "en")

# Database setup
engine = create_async_engine(DB_URL, future=True, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Initialize bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user.name}")

    # Ensure database tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database is ready.")
    print("Bot is ready to accept commands.")

# Load commands
async def setup_commands():
    async_session_instance = async_session()
    bot.add_cog(LocaleCommands(async_session_instance, default_locale=LOCALE))
    bot.add_cog(CitizenCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(CompanyCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(RegionCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(RoadCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(HousingCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(InsuranceCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(LoanCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(TradeCommands(async_session_instance, locale=LOCALE))
    bot.add_cog(PublicProjectCommands(async_session_instance, locale=LOCALE))
    print("Commands loaded.")

# Scheduled tasks
async def run_tasks():
    async_session_instance = async_session()
    guild = discord.utils.get(bot.guilds, name=os.getenv("GUILD_NAME"))

    if not guild:
        print("Guild not found. Tasks will not be run.")
        return

    # Example task scheduling (you can use a task scheduler like `aiocron` or custom loops)
    await update_region_economy(async_session_instance, guild)
    await process_insurance_payments(async_session_instance, guild)
    await process_loan_repayments(async_session_instance, guild)

# Bot startup
@bot.event
async def on_connect():
    await setup_commands()
    await run_tasks()

# Run bot
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")
    bot.run(TOKEN)
