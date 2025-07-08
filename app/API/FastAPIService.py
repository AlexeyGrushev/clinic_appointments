import uvicorn

from fastapi import FastAPI

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

    async def start(self) -> None:
        uvicorn_cfg = uvicorn.Config(
            self.app,
            host=self.settings.APP_HOST,
            port=self.settings.APP_PORT
        )
        server = uvicorn.Server(uvicorn_cfg)

        await server.serve()
