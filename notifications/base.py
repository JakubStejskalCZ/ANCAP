import discord
from utils.translator import Translator

class NotificationBase:
    """Base class for all notifications."""
    
    def __init__(self, guild: discord.Guild, locale="en"):
        self.guild = guild
        self.translator = Translator(locale)

    async def send(self):
        """Method to be overridden by specific notifications."""
        raise NotImplementedError("Each notification must implement its own send method.")
