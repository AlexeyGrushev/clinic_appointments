import asyncio

from app.ClinicAppointments import ClinicAppointments
from app.Core.Settings import settings


async def main() -> None:
    clinic_appointments = ClinicAppointments(settings=settings)
    await clinic_appointments.launch()

if __name__ == "__main__":
    asyncio.run(main())
