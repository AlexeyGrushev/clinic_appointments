from sqlalchemy.exc import IntegrityError

from app.API.Appointments.DAO import AppointmentDAO
from app.API.Appointments.schemas.AppointmentScheme import SAppointment
from app.API.http_exceptions import (
    http_exc_404_not_found,
    http_exc_409_conflict,
)
from app.Core.BaseRouter import BaseRouter


class AppointmentRouter(BaseRouter):
    def __init__(self, dao: AppointmentDAO, prefix: str, tags: list[str]):
        super().__init__(dao=dao, prefix=prefix, tags=tags)
        self.dao = dao

    def _register_routes(self):
        self._router.add_api_route(
            "/appointments/{appointment_id}",
            self._get_appointment,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/appointments/", self._add_appointment, methods=["POST"]
        )

    async def _get_appointment(self, appointment_id: int):
        data = await self.dao.find_one_or_none(id=appointment_id)
        if not data:
            raise http_exc_404_not_found
        return {
            "id": data[0].id,
            "doctor_id": data[0].doctor_id,
            "client_id": data[0].client_id,
            "start_time": data[0].start_time,
            "end_time": data[0].end_time,
            "note": data[0].note,
        }

    async def _add_appointment(self, data: SAppointment):
        try:
            appointment_id = await self.dao.insert_values(
                doctor_id=data.doctor_id,
                client_id=data.client_id,
                start_time=data.start_time,
                end_time=data.end_time,
                note=data.note,
            )
        except IntegrityError:
            raise http_exc_409_conflict
        return appointment_id

    def get_router(self):
        return super().get_router()
