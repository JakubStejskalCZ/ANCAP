from discord.ext import commands
from sqlalchemy import select
from models.employment import Job
from models.citizen import Citizen
from utils.translator import Translator

class EmploymentCommands(commands.Cog):
    def __init__(self, session, locale="en"):
        self.session = session
        self.translator = Translator(locale)

    @commands.command()
    async def create_job(self, ctx, title: str, salary: float, terms: str):
        """Create a new job listing."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Create the job
            job = Job(
                title=title,
                employer_id=citizen.id,
                salary=salary,
                terms=terms,
                is_open=True
            )
            session.add(job)
            await session.commit()

            # Notify user
            message = self.translator.translate("job_created", title=title, salary=salary)
            await ctx.send(message)

    @commands.command()
    async def list_jobs(self, ctx):
        """List all open job listings."""
        async with self.session() as session:
            jobs = await session.execute(select(Job).where(Job.is_open == True))
            jobs = jobs.scalars().all()

            if not jobs:
                message = self.translator.translate("no_jobs_found")
                await ctx.send(message)
                return

            response = "\n".join(
                [f"- {job.title} ({job.salary} ancapy/month): {job.terms}" for job in jobs]
            )
            message = self.translator.translate("job_list", jobs=response)
            await ctx.send(message)

    @commands.command()
    async def apply_job(self, ctx, job_id: int):
        """Apply for a job."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            # Retrieve job
            job = await session.get(Job, job_id)
            if not job or not job.is_open:
                message = self.translator.translate("job_not_found_or_closed")
                await ctx.send(message)
                return

            # Assign job to citizen
            citizen.is_employed = True
            job.is_open = False
            await session.commit()

            # Notify user
            message = self.translator.translate("job_applied", title=job.title)
            await ctx.send(message)

    @commands.command()
    async def quit_job(self, ctx):
        """Quit your current job."""
        async with self.session() as session:
            user_id = ctx.author.id

            # Validate citizen existence
            citizen = await session.execute(select(Citizen).where(Citizen.discord_id == user_id))
            citizen = citizen.scalars().first()
            if not citizen:
                message = self.translator.translate("citizen_not_found")
                await ctx.send(message)
                return

            if not citizen.is_employed:
                message = self.translator.translate("not_employed")
                await ctx.send(message)
                return

            # Update employment status
            citizen.is_employed = False
            await session.commit()

            # Notify user
            message = self.translator.translate("job_quit", name=citizen.name)
            await ctx.send(message)
