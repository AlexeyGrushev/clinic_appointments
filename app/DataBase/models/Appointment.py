from datetime import datetime

from sqlalchemy import VARCHAR, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.DataBase.Base import Base


class Appointment(Base):
    __tablename__ = "Appointment"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    doctor_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )
    client_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, unique=True
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    note: Mapped[str | None] = mapped_column(
        VARCHAR(255), nullable=True, unique=False
    )
