from notifications.base import NotificationBase
import discord

class FailedInsurancePaymentNotification(NotificationBase):
    def __init__(self, guild: discord.Guild, citizen_name: str, company_name: str, locale="en"):
        super().__init__(guild, locale)
        self.citizen_name = citizen_name
        self.company_name = company_name

    async def send(self):
        channel = discord.utils.get(self.guild.channels, name="general")
        if channel:
            message = self.translator.translate(
                "failed_insurance_payment",
                citizen_name=self.citizen_name,
                company_name=self.company_name
            )
            await channel.send(message)
        else:
            print(f"General channel not found in guild '{self.guild.name}'.")
