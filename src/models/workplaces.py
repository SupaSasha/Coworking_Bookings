import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm


class WorkplacesOrm(Base):
    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    coworking_id: Mapped[int] = mapped_column(ForeignKey("coworkings.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="workplaces",
        secondary="workplaces_facilities",
    )
