from discord.ext import commands
from sqlalchemy import select
from models.public_projects import PublicProject
from models.citizen import Citizen
from utils.translator import Translator

class PublicProjectCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_public_project(self, ctx, name: str, cost: float):
        """Create a new public project."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Create public project
            project = PublicProject(
                name=name,
                cost=cost,
                funds_raised=0.0,
                is_completed=False
            )
            session.add(project)
            await session.commit()

            # Notify user
            message = self.translator.translate("public_project_created", name=name, cost=cost)
            await ctx.send(message)

    @commands.command()
    async def list_public_projects(self, ctx):
        """List all public projects."""
        async with self.session() as session:
            projects = await session.execute(select(PublicProject))
            projects = projects.scalars().all()

            if not projects:
                message = self.translator.translate("no_public_projects_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [
                    f"- {project.name} | Cost: {project.cost} ancapy | Raised: {project.funds_raised} ancapy | "
                    f"Status: {'Completed' if project.is_completed else 'In Progress'}"
                    for project in projects
                ]
            )
            message = self.translator.translate("public_project_list", projects=response)
            await ctx.send(message)

    @commands.command()
    async def fund_public_project(self, ctx, project_id: int, amount: float):
        """Fund a public project."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Validate citizen's balance
            if citizen.balance < amount:
                message = self.translator.translate("insufficient_balance")
                await ctx.send(message)
                return

            # Retrieve project
            project = await session.get(PublicProject, project_id)
            if not project or project.is_completed:
                message = self.translator.translate("project_not_found_or_completed")
                await ctx.send(message)
                return

            # Fund project
            project.funds_raised += amount
            citizen.balance -= amount

            # Check if project is completed
            if project.funds_raised >= project.cost:
                project.is_completed = True
                completion_message = self.translator.translate("public_project_completed", name=project.name)
                await ctx.send(completion_message)

            await session.commit()

            # Notify user
            message = self.translator.translate(
                "public_project_funded", name=project.name, amount=amount, raised=project.funds_raised, cost=project.cost
            )
            await ctx.send(message)
