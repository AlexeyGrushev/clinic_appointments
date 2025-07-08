from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, Field


class SAppointment(BaseModel):
    doctor_id: int
    client_id: int
    start_time: datetime = datetime.now(timezone.utc)
    end_time: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
    note: Optional[str] = Field(default=None, max_length=255)
