import pytest
from app.API.Appointments.Router import AppointmentRouter

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

from app.Core.Logger import Logger


@pytest.fixture
def mock_dao():
    mock = AsyncMock()
    return mock


@pytest.fixture
def router(mock_dao):
    return AppointmentRouter(
        dao=mock_dao,
        prefix="/api",
        tags=["Appointments"],
        logger=Logger(
            filename="fastapi-test.log",
            level="DEBUG"
        )
    )


@pytest.mark.asyncio
async def test_get_appointment_found(router, mock_dao):
    mock_dao.find_one_or_none.return_value = [type("Appointment", (), {
        "id": 1,
        "doctor_id": 123,
        "client_id": 456,
        "start_time": datetime.now(timezone.utc),
        "end_time": datetime.now(timezone.utc) + timedelta(minutes=15),
        "note": "Unit-test note"
    })]

    result = await router._get_appointment(1)
    assert result["id"] == 1
    assert result["doctor_id"] == 123
