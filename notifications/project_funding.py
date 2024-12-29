from notifications.base import NotificationBase
import discord

class ProjectFundingNotification(NotificationBase):
    def __init__(self, guild: discord.Guild, project_name: str, locale="en"):
        super().__init__(guild, locale)
        self.project_name = project_name

    async def send(self):
        channel = discord.utils.get(self.guild.channels, name="general")
        if channel:
            message = self.translator.translate(
                "project_funding_completed",
                project_name=self.project_name
            )
            await channel.send(message)
        else:
            print(f"General channel not found in guild '{self.guild.name}'.")
