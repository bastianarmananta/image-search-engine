import os
from utils.logger import logging
from fastapi import APIRouter, status
from src.schema.request_format import StartEncoderTask
from src.schema.response import ResponseDefault, EncoderState
from src.exceptions import NotFoundError
from services.celery.app import grab_all_images

router = APIRouter(tags=["Encoder"])


async def start_encoder(schema: StartEncoderTask) -> ResponseDefault:
    logging.info("Endpoint Start Encoder.")
    response = ResponseDefault()
    state = EncoderState()

    if not os.path.exists(path=schema.data_path):
        raise NotFoundError(detail="Directory is not available on project")

    data_path_str = str(schema.data_path)
    task = grab_all_images.delay(root_dir=data_path_str)
    state.task_id = task.id

    response.message = "Task has been queued."
    response.data = state

    return response


router.add_api_route(
    methods=["POST"],
    path="/encoder-start",
    endpoint=start_encoder,
    summary="Start encoder task.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
