import time
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from datetime import datetime
from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from utils.logger import logging
from src.exceptions import ImageSearchEngineApiError, NotFoundError


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


async def grab_all_images(root_dir: str) -> list | None:
    """
    Recursively extracting all image path based on root path dir.

    Parameters:
    - root_path: Root directory for searching image data.

    Returns:
    - List of all image data in extension jpg, jpeg, png.
    """
    start_time = local_time()
    if not os.path.exists(path=root_dir):
        raise NotFoundError(
            detail=f"[grab_all_images] Directory {root_dir} not available, make sure its mounted or available in projects directory."
        )

    image_extensions = {".jpg", ".jpeg", ".png"}
    time.sleep(120)
    image_paths = [
        str(path)
        for path in Path(root_dir).rglob("*")
        if path.suffix.lower() in image_extensions
    ]

    if not image_paths:
        raise NotFoundError(
            detail=f"[grab_all_images] No image files found in {root_dir}"
        )
    end_time = local_time()
    logging.info(f"[grab_all_images] Elapsed grab all image: {end_time - start_time}")

    return image_paths
