from notifications.base import NotificationBase
import discord

class FailedLoanPaymentNotification(NotificationBase):
    def __init__(self, guild: discord.Guild, borrower_name: str, lender_name: str, loan_id: int, locale="en"):
        super().__init__(guild, locale)
        self.borrower_name = borrower_name
        self.lender_name = lender_name
        self.loan_id = loan_id

    async def send(self):
        channel = discord.utils.get(self.guild.channels, name="general")
        if channel:
            message = self.translator.translate(
                "failed_loan_payment",
                borrower_name=self.borrower_name,
                lender_name=self.lender_name,
                loan_id=self.loan_id
            )
            await channel.send(message)
        else:
            print(f"General channel not found in guild '{self.guild.name}'.")
