from pydantic import BaseModel


class StartEncoderTask(BaseModel):
    data_path: str
