from pathlib import Path
from pydantic import BaseModel


class StartEncoderTask(BaseModel):
    data_path: Path


class CheckEncoderState(BaseModel):
    task_id: str
