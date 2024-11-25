from utils.logger import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health Check"])


async def root():
    logging.info("Endpoint Root.")
    return JSONResponse(content={"status": "Server running!"})


router.add_api_route(
    methods=["GET"],
    path="/",
    endpoint=root,
    summary="Health check.",
    status_code=status.HTTP_200_OK,
)
