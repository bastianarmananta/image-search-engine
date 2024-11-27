from datetime import datetime
from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from utils.logger import logging
from src.exceptions import ImageSearchEngineApiError


def create_exception_handler(
    status_code: int, detail_message: str
) -> Callable[[Request, ImageSearchEngineApiError], JSONResponse]:
    detail = {"message": detail_message}

    async def exception_handler(
        _: Request, exc: ImageSearchEngineApiError
    ) -> JSONResponse:
        if exc:
            detail["message"] = exc.detail

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        logging.error(exc)
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler


def local_time() -> datetime:
    return datetime.now()
