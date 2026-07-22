from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import FacilitiesRepository, WorkplacesFacilitiesRepository
from src.repositories.coworkings import CoworkingsRepository
from src.repositories.workplaces import WorkplacesRepository
from src.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.coworkings = CoworkingsRepository(self.session)
        self.workplaces = WorkplacesRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.workplaces_facilities = WorkplacesFacilitiesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
