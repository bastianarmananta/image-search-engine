from pydantic import BaseModel
from typing import Union


class ResponseDefault(BaseModel):
    success: bool = True
    message: str = None
    data: Union[list, str, dict] = None


class EncoderState(BaseModel):
    task_id: str = ""


class TaskResultState(BaseModel):
    task_id: str = ""
    status: str = None
    result: Union[list, str, dict] = None
