from enum import Enum
from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field
from services.postgre.connection import database_connection


class StatusEnum(str, Enum):
    standby = "standby"
    on_process = "on_process"
    finished = "finished"


class EncoderState(SQLModel, table=True):
    __tablename__ = "encoder_state"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    elapsed_encoding_time: datetime | None = Field(default=None)
    unique_id: str = Field(max_length=255)
    encoder_name: str | None = Field(max_length=255, default=None)
    status: StatusEnum = Field(default="standby")
    is_finished: bool = Field(default=False)


class ImageClassification(SQLModel, table=True):
    __tablename__ = "image_classification"
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    image_path: str | None = Field(default=None)
    image_name: str | None = Field(default=None)
    tag_id: str | None = Field(default=None, max_length=255)


async def database_migration():
    engine = await database_connection()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
