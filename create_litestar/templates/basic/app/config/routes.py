"""Ingestion point for all app routes, to be sent into the Litestar app instance."""

from litestar.types import ControllerRouterHandler

from app.domain.system.controllers import SystemController

__all__ = ("route_handlers",)

route_handlers: list[ControllerRouterHandler] = [SystemController]
