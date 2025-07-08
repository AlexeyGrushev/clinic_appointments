from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException

from app.API.Appointments.DAO import AppointmentDAO
from app.API.Appointments.Router import AppointmentRouter
from app.Core.Settings import Settings
from app.Logger import Logger


class FastAPIService:
    """
    FastAPIService class for creating and managing a FastAPI application.
    """

    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.settings = settings
        self.logger = logger
        self.app = FastAPI(
            title=self.settings.APP_NAME,
        )
        self.appointment_router = AppointmentRouter(
            dao=AppointmentDAO(),
            prefix=self.settings.APP_PREFIX,
            tags=["Appointments"],
        )
        self._register_routes()

    def _register_routes(self) -> None:
        self.app.add_api_route(
            path="/health",
            endpoint=self._health_check,
            methods=["GET"],
            tags=["Health Check"],
        )

        self.app.include_router(self.appointment_router.get_router())

    async def __check_db_connectivity(self) -> bool:
        try:
            model = AppointmentDAO()
            result = await model.find_max_id()
            if isinstance(result.fetchone()[0], int):
                return True
            else:
                return False
        except Exception:
            return False

    async def __check_app_health(self) -> bool:
        return True

    async def _health_check(self) -> dict[str | Any, Any]:
        app_health = await self.__check_app_health()
        db_health = await self.__check_db_connectivity()
        status = app_health and db_health
        result = {
            "app_health": app_health,
            "db_health": db_health,
            "status": "ok" if status else "unavailable",
        }
        if not status:
            raise HTTPException(status_code=503, detail=result)

        return result

    async def start(self) -> None:
        uvicorn_cfg = uvicorn.Config(
            self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT
        )
        server = uvicorn.Server(uvicorn_cfg)

        await server.serve()
