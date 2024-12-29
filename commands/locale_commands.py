from discord.ext import commands
from sqlalchemy import select, update
from models.user_preferences import UserPreferences
from utils.translator import Translator

class LocaleCommands(commands.Cog):
    def __init__(self, session, default_locale="en"):
        self.session = session
        self.default_locale = default_locale
        self.translator = Translator(default_locale)

    @commands.command(name="set_locale")
    async def set_locale(self, ctx, locale: str):
        """
        Command to change the locale for the user dynamically and persist it in the database.
        :param ctx: Command context
        :param locale: The locale to set (e.g., 'en', 'cs')
        """
        valid_locales = ["en", "cs"]  # Extend this list for additional locales
        if locale not in valid_locales:
            message = self.translator.translate("invalid_locale", locales=", ".join(valid_locales))
            await ctx.send(message)
            return

        async with self.session() as session:
            # Check if the user already has preferences
            query = select(UserPreferences).where(UserPreferences.discord_id == ctx.author.id)
            result = await session.execute(query)
            preferences = result.scalars().first()

            if preferences:
                # Update existing preferences
                preferences.locale = locale
            else:
                # Create new preferences
                new_preferences = UserPreferences(discord_id=ctx.author.id, locale=locale)
                session.add(new_preferences)

            await session.commit()

        message = self.translator.translate("locale_set", locale=locale)
        await ctx.send(message)

    @commands.command(name="get_locale")
    async def get_locale(self, ctx):
        """
        Command to display the current locale for the user.
        :param ctx: Command context
        """
        async with self.session() as session:
            query = select(UserPreferences).where(UserPreferences.discord_id == ctx.author.id)
            result = await session.execute(query)
            preferences = result.scalars().first()

            locale = preferences.locale if preferences else self.default_locale
            message = self.translator.translate("current_locale", locale=locale)
            await ctx.send(message)

    async def get_user_locale(self, user_id):
        """
        Retrieve the locale for a specific user from the database, or use the default.
        :param user_id: The Discord user ID
        :return: The locale as a string
        """
        async with self.session() as session:
            query = select(UserPreferences).where(UserPreferences.discord_id == user_id)
            result = await session.execute(query)
            preferences = result.scalars().first()
            return preferences.locale if preferences else self.default_locale
