from notifications.base import NotificationBase
import discord

class InsuranceRequestNotification(NotificationBase):
    def __init__(self, guild: discord.Guild, citizen_name: str, company_name: str, owner_discord_id: int, locale="en"):
        super().__init__(guild, locale)
        self.citizen_name = citizen_name
        self.company_name = company_name
        self.owner_discord_id = owner_discord_id

    async def send(self):
        user = self.guild.get_member(self.owner_discord_id)
        if user:
            message = self.translator.translate(
                "insurance_request",
                citizen_name=self.citizen_name,
                company_name=self.company_name
            )
            await user.send(message)
        else:
            print(f"Company owner with Discord ID {self.owner_discord_id} not found.")
