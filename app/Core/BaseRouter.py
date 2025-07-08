from abc import ABC, abstractmethod
from typing import Any

from fastapi import APIRouter


class BaseRouter(ABC):
    def __init__(
        self,
        tags: list,
        prefix: str,
        dao: Any = None,
    ):
        self._router = APIRouter(prefix=prefix, tags=tags)
        self.dao = dao
        self._register_routes()

    @abstractmethod
    def _register_routes(self) -> None:
        """Register routes for the router"""
        pass

    def get_router(self) -> APIRouter:
        """Get the APIRouter instance"""
        return self._router
