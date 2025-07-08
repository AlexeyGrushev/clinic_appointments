from abc import ABC, abstractmethod
from enum import Enum
from fastapi import APIRouter
from typing import TypeVar, Generic

D = TypeVar('D')  # DAO
S = TypeVar('S')  # Pydantic Scheme


class BaseRouter(ABC, Generic[D, S]):
    def __init__(
        self,
        dao: D,
        prefix: str,
        tags: list[str | Enum]
    ):
        self.router = APIRouter(
            prefix=prefix,
            tags=tags
        )
        self.dao = dao
        self._register_routes()

    @abstractmethod
    def _register_routes(self) -> None:
        """Register routes for the router"""
        pass

    def get_router(self) -> APIRouter:
        """Get the APIRouter instance"""
        return self.router
