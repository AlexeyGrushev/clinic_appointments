from app.API.FastAPIService import FastAPIService
from app.Core.Settings import Settings
from app.Logger import Logger


class ClinicAppointments:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.__fastapi_service = FastAPIService(
            settings=self.settings,
            logger=Logger(
                filename=self.settings.APP_LOGGER_NAME,
                level=self.settings.LOG_LEVEL,
            ),
        )

    async def launch(self) -> None:
        """Launch services"""
        await self.__fastapi_service.start()
