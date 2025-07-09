from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException

from app.API.Appointments.DAO import AppointmentDAO
from app.API.Appointments.Router import AppointmentRouter
from app.Core.Logger import Logger
from app.Core.Settings import Settings


class FastAPIService:
    """
    FastAPIService class for creating and managing a FastAPI application.
    """

    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.settings = settings
        self.logger = logger
        self.logger.info("Initializing FastAPIService")

        self.app = FastAPI(
            title=self.settings.APP_NAME,
        )
        self.appointment_router = AppointmentRouter(
            dao=AppointmentDAO(),
            prefix=self.settings.APP_PREFIX,
            tags=["Appointments"],
            logger=self.logger,
        )
        self._register_routes()
        self.logger.info("FastAPIService initialized and routes registered")

    def _register_routes(self) -> None:
        self.logger.debug("Registering routes")
        self.app.add_api_route(
            path="/health",
            endpoint=self._health_check,
            methods=["GET"],
            tags=["Health Check"],
        )
        self.app.include_router(self.appointment_router.get_router())
        self.logger.debug("Routes registered successfully")

    async def __check_db_connectivity(self) -> bool:
        self.logger.debug("Checking database connectivity")
        try:
            model = AppointmentDAO()
            result = await model.ping()
            if result == 1:
                self.logger.debug("Database connectivity check passed")
                return True
            else:
                self.logger.warning(
                    "Database connectivity check failed: result not int"
                )
                return False
        except Exception as e:
            self.logger.error(f"Database connectivity check failed: {e}")
            return False

    async def __check_app_health(self) -> bool:
        self.logger.debug("Checking app health")
        return True

    async def _health_check(self) -> dict[str | Any, Any]:
        self.logger.info("Health check requested")
        app_health = await self.__check_app_health()
        db_health = await self.__check_db_connectivity()
        status = app_health and db_health
        result = {
            "app_health": app_health,
            "db_health": db_health,
            "status": "ok" if status else "unavailable",
        }
        if not status:
            self.logger.warning(f"Health check failed: {result}")
            raise HTTPException(status_code=503, detail=result)

        self.logger.info(f"Health check passed: {result}")
        return result

    async def start(self) -> None:
        self.logger.info(
            f"Starting server at {
                self.settings.APP_HOST}:{self.settings.APP_PORT}"
        )
        uvicorn_cfg = uvicorn.Config(
            self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT
        )
        server = uvicorn.Server(uvicorn_cfg)

        await server.serve()
        self.logger.info("Server stopped")
