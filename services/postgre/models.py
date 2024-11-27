from datetime import datetime
from utils.helper import local_time
from sqlmodel import SQLModel, Field, Relationship
from services.postgre.connection import database_connection


class EncoderInformation(SQLModel, table=True):
    __tablename__ = "model_information"

    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    unique_id: str = Field(max_length=255, unique=True)
    encoder_name: str = Field(max_length=255, default=None)
    data_source: str = Field(max_length=255, default=None)
    image_trained: int = Field(default=None)
    total_image_data: int = Field(default=None)
    elapsed_encoding_time: datetime = Field(default=None)
    should_re_encode: bool = Field(default=False)

    details: list["EncoderDetails"] = Relationship(back_populates="information")


class EncoderDetails(SQLModel, table=True):
    __tablename__ = "model_details"

    id: int = Field(primary_key=True)
    unique_id: str = Field(foreign_key="model_information.unique_id", max_length=255)
    created_at: datetime = Field(default=local_time())
    updated_at: datetime | None = Field(default=None)
    image_path: str = Field(default=None)
    image_name: str = Field(default=None)
    tag_id: str = Field(default=None, max_length=255)

    information: EncoderInformation = Relationship(back_populates="details")


async def database_migration():
    engine = await database_connection()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
