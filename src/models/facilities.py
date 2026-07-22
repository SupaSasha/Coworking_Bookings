import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import WorkplacesOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    workplaces: Mapped[list["WorkplacesOrm"]] = relationship(
        back_populates="facilities",
        secondary="workplaces_facilities",
    )


class WorkplacesFacilitiesOrm(Base):
    __tablename__ = "workplaces_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
