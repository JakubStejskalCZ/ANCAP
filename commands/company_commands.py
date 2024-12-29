from discord.ext import commands
from sqlalchemy import select
from models.company import Company, CompanyType
from models.citizen import Citizen
from utils.translator import Translator
from notifications.base import NotificationBase

class CompanyCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_company(self, ctx, name: str, company_type: str):
        """Create a new company."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Validate company type
            try:
                company_type_enum = CompanyType(company_type.lower())
            except ValueError:
                message = self.translator.translate("invalid_company_type", types=", ".join([e.value for e in CompanyType]))
                await ctx.send(message)
                return

            # Create the company
            company = Company(
                name=name,
                owner_id=citizen.id,
                company_type=company_type_enum
            )
            session.add(company)
            await session.commit()

            # Notify user
            success_message = self.translator.translate("company_created", name=name, company_type=company_type_enum.value)
            await ctx.send(success_message)

    @commands.command()
    async def list_companies(self, ctx, company_type: str = None):
        """List all companies or filter by type."""
        async with self.session() as session:
            query = select(Company)
            if company_type:
                try:
                    company_type_enum = CompanyType(company_type.lower())
                    query = query.where(Company.company_type == company_type_enum)
                except ValueError:
                    message = self.translator.translate("invalid_company_type", types=", ".join([e.value for e in CompanyType]))
                    await ctx.send(message)
                    return

            companies = await session.execute(query)
            companies_list = companies.scalars().all()

            if not companies_list:
                message = self.translator.translate("no_companies_found")
                await ctx.send(message)
                return

            response = self.translator.translate("companies_list", companies="\n".join([f"- {company.name} ({company.company_type.value})" for company in companies_list]))
            await ctx.send(response)

    @commands.command()
    async def delete_company(self, ctx, company_id: int):
        """Delete a company owned by the user."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve and validate company ownership
            company = await session.get(Company, company_id)
            if not company or company.owner_id != citizen.id:
                message = self.translator.translate("company_not_found_or_not_owner")
                await ctx.send(message)
                return

            # Delete company
            session.delete(company)
            await session.commit()

            # Notify user
            message = self.translator.translate("company_deleted", name=company.name)
            await ctx.send(message)
