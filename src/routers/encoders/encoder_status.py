from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from src.schema.response import ResponseDefault, TaskResultState
from services.celery.app import app
from utils.logger import logging

router = APIRouter(tags=["Encoder"])


async def check_task_status(task_id: str) -> ResponseDefault:
    """
    Endpoint to check the status and result of a queued task using task_id.

    Parameters:
    - task_id: The ID of the Celery task.

    Returns:
    - ResponseDefault containing task status and result (if completed).
    """
    logging.info(f"Checking status for task_id: {task_id}")
    response = ResponseDefault()
    state = TaskResultState()

    # Retrieve the task using the task_id
    task_result = AsyncResult(task_id, app=app)

    # Check if the task is valid
    if task_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found.",
        )

    # Populate state with task information
    state.task_id = task_id
    state.status = task_result.status

    # If task is completed, include the result
    if task_result.status == "SUCCESS":
        state.result = task_result.result
    elif task_result.status == "FAILURE":
        state.error_message = str(task_result.result)  # Error details if failed

    response.message = f"Task status for {task_id} is {task_result.status}."
    response.data = state
    return response


router.add_api_route(
    methods=["GET"],
    path="/task-status/{task_id}",
    endpoint=check_task_status,
    summary="Check task status and result.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
