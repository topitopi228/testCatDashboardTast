from core.db_helper import db_helper
from core.models.base import Base


async def create_tables():
    from core.models import base, mission,spy_cat,target
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        db_helper.engine.echo = True