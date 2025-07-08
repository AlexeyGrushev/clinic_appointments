import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient

from app.API.FastAPIService import FastAPIService
from app.Core.Settings import settings
from app.Logger import Logger

fastapi = FastAPIService(
    settings=settings,
    logger=Logger(
        filename="fastapi-test.log",
        level="DEBUG"
    )
)

client = TestClient(fastapi.app)


@pytest.fixture
def appointment_payload():
    now = datetime.now(timezone.utc)
    return {
        "doctor_id": 1,
        "client_id": 2,
        "start_time": now.isoformat(),
        "end_time": (now + timedelta(minutes=15)).isoformat(),
        "note": "Integration test",
    }


def test_create_appointment_with_possible_conflict(appointment_payload):
    response = client.post(
        f"{settings.APP_PREFIX}/appointments/", json=appointment_payload)
    assert response.status_code in [
        201, 409], f"Unexpected status: {response.status_code}"
