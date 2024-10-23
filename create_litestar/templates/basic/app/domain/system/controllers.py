from __future__ import annotations

from typing import Literal, TypeVar

import structlog
from litestar import Controller, MediaType, Request, get
from litestar.response import Response

from app.config.settings import get_settings

from .schemas import SystemInfo
from .urls import SYSTEM_INFO


logger = structlog.get_logger()
OnlineOffline = TypeVar("OnlineOffline", bound=Literal["online", "offline"])


class SystemController(Controller):
    tags = ["System"]

    @get(
        operation_id="SystemHealth",
        name="system:info",
        path=SYSTEM_INFO,
        media_type=MediaType.JSON,
        cache=False,
        tags=["System"],
        summary="Info",
        description="Returns info about the API",
    )
    async def check_system_info(
        self,
        request: Request,
    ) -> Response[SystemInfo]:
        """Check database available and returns app config info."""
        settings = get_settings()

        return Response(
            content=SystemInfo(name=settings.app.NAME),  # type: ignore
            status_code=200,
            media_type=MediaType.JSON,
        )
