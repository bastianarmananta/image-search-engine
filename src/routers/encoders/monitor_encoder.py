from uuid import UUID
from utils.logger import logging
from celery.result import AsyncResult
from services.celery.worker import app
from fastapi import APIRouter, status
from src.schema.response import ResponseDefault, TaskResultState

router = APIRouter(tags=["Encoder"])


async def status_encoder(task_id: UUID) -> ResponseDefault:
    """
    Check the status and result of a queued task using task_id.

    Parameters:
    - task_id: The ID of the Celery task.

    Returns:
    - Returned status and result based on respective celery task_id.
    """
    logging.info(f"Checking status for task_id: {task_id}")
    response = ResponseDefault()
    state = TaskResultState()

    task_result = AsyncResult(id=str(task_id), app=app)

    state.task_id = str(task_id)
    state.status = task_result.status
    state.result = task_result.result

    response.message = f"Retrieved information from task_id {task_id}."
    response.data = state
    return response


router.add_api_route(
    methods=["GET"],
    path="/encoder-status/{task_id}",
    endpoint=status_encoder,
    summary="Check task status and result.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
