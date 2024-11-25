from utils.logger import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Encoder"])


async def start_encoder():
    logging.info("Endpoint Start Encoder.")
    return JSONResponse(content={"status": "Server running!"})


router.add_api_route(
    methods=["POST"],
    path="/encoder-start",
    endpoint=start_encoder,
    summary="Start encoder task.",
    status_code=status.HTTP_200_OK,
)
