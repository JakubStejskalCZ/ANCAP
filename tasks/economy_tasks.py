import random
from sqlalchemy import select
from models.region import Region
from notifications.prosperity_change import ProsperityChangeNotification

async def update_region_economy(session, guild):
    """
    Periodically update prosperity and pollution levels in all regions.
    Adjustments are random within defined ranges.
    """
    async with session() as session:
        regions = await session.execute(select(Region))
        for region in regions.scalars().all():
            old_prosperity = region.prosperity
            old_pollution = region.pollution

            # Adjust prosperity and pollution
            region.prosperity += random.uniform(-2, 3)  # Random prosperity adjustment
            region.pollution += random.uniform(-1, 2)  # Random pollution adjustment

            # Ensure values stay within valid bounds
            region.prosperity = max(0, region.prosperity)
            region.pollution = max(0, region.pollution)

            # Notify about prosperity change if significant
            if abs(region.prosperity - old_prosperity) > 0.1:  # Threshold for notification
                notification = ProsperityChangeNotification(
                    guild=guild,
                    region_name=region.name,
                    old_prosperity=old_prosperity,
                    new_prosperity=region.prosperity
                )
                await notification.send()

            # Log pollution changes for debugging or tracking
            print(
                f"Region '{region.name}': Prosperity {old_prosperity:.2f} -> {region.prosperity:.2f}, "
                f"Pollution {old_pollution:.2f} -> {region.pollution:.2f}"
            )

        await session.commit()
