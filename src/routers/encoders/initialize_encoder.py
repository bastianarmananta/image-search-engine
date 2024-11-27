import os
from fastapi import APIRouter, status
from src.exceptions import NotFoundError
from services.celery.tasks import start_encoder_task
from src.schema.request_format import StartEncoderTask
from src.schema.response import ResponseDefault, TaskResultState

router = APIRouter(tags=["Encoder"])


async def start_encoder(schema: StartEncoderTask) -> ResponseDefault:
    response = ResponseDefault()
    state = TaskResultState()

    if not os.path.exists(path=schema.data_path):
        raise NotFoundError(detail="Directory is not available on project.")

    task = start_encoder_task.delay(root_path=schema.data_path)

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
