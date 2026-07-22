from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class CoworkingsOrm(Base):
    __tablename__ = "coworkings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
