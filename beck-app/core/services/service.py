from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.spy_cat import Cat, Mission, Breed
from core.models.target import Target
import requests

class SpyCatService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_cat(self, cat_id: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Cat).filter(Cat.id == cat_id))
            return result.scalars().first()

    async def get_cats(self, skip: int = 0, limit: int = 100):
        async with self.session_factory() as session:
            result = await session.execute(select(Cat).offset(skip).limit(limit))
            return result.scalars().all()

    async def create_cat(self, cat: dict):
        async with self.session_factory() as session:
            # Validate breed with TheCatAPI
            response = requests.get("https://api.thecatapi.com/v1/breeds", params={"name": cat["breed"]})
            if response.status_code != 200 or not response.json():
                raise ValueError("Invalid breed")
            db_cat = Cat(**cat)
            session.add(db_cat)
            await session.commit()
            await session.refresh(db_cat)
            return db_cat

    async def update_cat(self, cat_id: int, salary: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Cat).filter(Cat.id == cat_id))
            db_cat = result.scalars().first()
            if db_cat:
                db_cat.salary = salary
                await session.commit()
                await session.refresh(db_cat)
            return db_cat

    async def delete_cat(self, cat_id: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Cat).filter(Cat.id == cat_id))
            db_cat = result.scalars().first()
            if db_cat:
                await session.delete(db_cat)
                await session.commit()
            return db_cat

    async def create_mission(self, mission: dict, cat_id: int | None = None):
        async with self.session_factory() as session:
            if cat_id:
                result = await session.execute(select(Cat).filter(Cat.id == cat_id))
                cat = result.scalars().first()
                result = await session.execute(select(Mission).filter(Mission.cat_id == cat_id, Mission.is_complete == False))
                if not cat or result.scalars().first():
                    raise ValueError("Cat is unavailable")
            db_mission = Mission(cat_id=cat_id, is_complete=False)
            session.add(db_mission)
            await session.commit()
            await session.refresh(db_mission)
            for target_data in mission.get("targets", []):
                db_target = Target(**target_data, mission_id=db_mission.id)
                session.add(db_target)
            await session.commit()
            return db_mission

    async def update_target(self, mission_id: int, target_id: int, target_update: dict):
        async with self.session_factory() as session:
            result = await session.execute(select(Target).filter(Target.id == target_id, Target.mission_id == mission_id))
            target = result.scalars().first()
            result = await session.execute(select(Mission).filter(Mission.id == mission_id))
            mission = result.scalars().first()
            if not target or target.is_complete or mission.is_complete:
                raise ValueError("Target or mission is already completed")
            if "notes" in target_update:
                target.notes = target_update["notes"]
            if "is_complete" in target_update:
                target.is_complete = target_update["is_complete"]
                if target.is_complete and all(t.is_complete for t in mission.targets):
                    mission.is_complete = True
            await session.commit()
            await session.refresh(target)
            return target

    async def assign_cat_to_mission(self, mission_id: int, cat_id: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Mission).filter(Mission.id == mission_id))
            mission = result.scalars().first()
            if not mission or mission.cat_id or mission.is_complete:
                raise ValueError("Mission is unavailable")
            result = await session.execute(select(Cat).filter(Cat.id == cat_id))
            cat = result.scalars().first()
            result = await session.execute(select(Mission).filter(Mission.cat_id == cat_id, Mission.is_complete == False))
            if not cat or result.scalars().first():
                raise ValueError("Cat is unavailable")
            mission.cat_id = cat_id
            await session.commit()
            await session.refresh(mission)
            return mission

    async def get_missions(self, skip: int = 0, limit: int = 100):
        async with self.session_factory() as session:
            result = await session.execute(select(Mission).offset(skip).limit(limit))
            return result.scalars().all()

    async def get_mission(self, mission_id: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Mission).filter(Mission.id == mission_id))
            return result.scalars().first()

    async def delete_mission(self, mission_id: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Mission).filter(Mission.id == mission_id))
            mission = result.scalars().first()
            if mission and mission.cat_id:
                raise ValueError("Mission is assigned to a cat and cannot be deleted")
            if mission:
                await session.delete(mission)
                await session.commit()
            return mission

