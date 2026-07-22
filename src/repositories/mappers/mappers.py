from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, WorkplacesFacilitiesOrm
from src.models.coworkings import CoworkingsOrm
from src.models.workplaces import WorkplacesOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, WorkplaceFacility
from src.schemas.coworkings import Coworking
from src.schemas.workplaces import Workplace, WorkplaceWithRels
from src.schemas.users import User


class CoworkingDataMapper(DataMapper):
    db_model = CoworkingsOrm
    schema = Coworking


class WorkplaceDataMapper(DataMapper):
    db_model = WorkplacesOrm
    schema = Workplace


class WorkplaceDataWithRelsMapper(DataMapper):
    db_model = WorkplacesOrm
    schema = WorkplaceWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class WorkplaceFacilityDataMapper(DataMapper):
    db_model = WorkplacesFacilitiesOrm
    schema = WorkplaceFacility
