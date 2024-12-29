from notifications.base import NotificationBase
import discord

class ProsperityChangeNotification(NotificationBase):
    def __init__(self, guild: discord.Guild, region_name: str, old_prosperity: float, new_prosperity: float, locale="en"):
        super().__init__(guild, locale)
        self.region_name = region_name
        self.old_prosperity = old_prosperity
        self.new_prosperity = new_prosperity

    async def send(self):
        channel = discord.utils.get(self.guild.channels, name=self.region_name.lower())
        if channel:
            message = self.translator.translate(
                "prosperity_update",
                region_name=self.region_name,
                old=self.old_prosperity,
                new=self.new_prosperity
            )
            await channel.send(message)
        else:
            print(f"Channel '{self.region_name}' not found in guild '{self.guild.name}'.")
