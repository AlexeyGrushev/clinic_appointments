from fastapi.responses import JSONResponse

from app.API.Appointments.DAO import AppointmentDAO
from app.API.Appointments.schemas.AppointmentScheme import SAppointment
from app.API.http_exceptions import (
    http_exc_404_not_found,
    http_exc_409_conflict,
)
from app.Core.BaseRouter import BaseRouter
from app.Core.Logger import Logger


class AppointmentRouter(BaseRouter):
    def __init__(
        self, dao: AppointmentDAO, prefix: str, tags: list[str], logger: Logger
    ):
        super().__init__(dao=dao, prefix=prefix, tags=tags, logger=logger)
        self.dao = dao
        self.logger = logger
        self.logger.info("AppointmentRouter initialized")

    def _register_routes(self):
        self.logger.debug("Registering appointment routes")
        self._router.add_api_route(
            "/appointments/{appointment_id}",
            self._get_appointment,
            methods=["GET"],
        )
        self._router.add_api_route(
            "/appointments/", self._add_appointment, methods=["POST"]
        )
        self.logger.debug("Appointment routes registered")

    async def _get_appointment(self, appointment_id: int):
        self.logger.info(f"GET /appointments/{appointment_id} called")
        data = await self.dao.find_one_or_none(id=appointment_id)
        if not data:
            self.logger.warning(
                f"Appointment with id={appointment_id} not found"
            )
            raise http_exc_404_not_found

        appointment = {
            "id": data[0].id,
            "doctor_id": data[0].doctor_id,
            "client_id": data[0].client_id,
            "start_time": data[0].start_time,
            "end_time": data[0].end_time,
            "note": data[0].note,
        }
        self.logger.debug(f"Appointment data retrieved: {appointment}")
        return appointment

    async def _add_appointment(self, data: SAppointment):
        self.logger.info(
            f"POST /appointments/ called with data: doctor_id={
                data.doctor_id}, "
            f"start_time={data.start_time}"
        )
        existing = await self.dao.find_one_or_none(
            doctor_id=data.doctor_id,
            start_time=data.start_time,
        )
        if existing:
            self.logger.warning(
                f"Conflict: Appointment already exists for doctor_id={
                    data.doctor_id} "
                f"at start_time={data.start_time}"
            )
            raise http_exc_409_conflict

        appointment_id = await self.dao.insert_values(
            doctor_id=data.doctor_id,
            client_id=data.client_id,
            start_time=data.start_time,
            end_time=data.end_time,
            note=data.note,
        )
        self.logger.info(f"Appointment created with id={appointment_id}")
        return JSONResponse(content={"id": appointment_id}, status_code=201)

    def get_router(self):
        return super().get_router()
