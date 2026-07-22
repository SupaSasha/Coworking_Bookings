from src.schemas.coworkings import CoworkingAdd
from src.utils.db_manager import DBManager


async def test_add_coworking(db: DBManager):
    coworking_data = CoworkingAdd(title="Coworking 5 stars", location="Montevideo")
    await db.coworkings.add(coworking_data)
    await db.commit()
