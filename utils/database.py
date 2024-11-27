# TODO: sample code, refactor immediately
import sys
import asyncio
from pathlib import Path
import uuid  # Import uuid for generating unique IDs

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.helper import local_time
from services.postgre.connection import database_connection
from services.postgre.models import EncoderInformation, EncoderDetails
from sqlalchemy import insert


async def save_model_info() -> str:
    # Create a new EncoderInformation instance with mock data and use uuid4 for the unique_id
    new_encoder_info = EncoderInformation(
        unique_id=str(uuid.uuid4()),  # Generate a new unique ID using uuid4
        encoder_name="Test Encoder",
        data_source="Test Data Source",
        image_trained=100,
        total_image_data=500,
        elapsed_encoding_time=local_time(),  # Assuming this is a datetime value
        should_re_encode=False,
    )

    # Get the database engine
    engine = await database_connection()

    # Insert the new data into the database
    async with engine.begin() as conn:
        # Use execute with an insert statement
        stmt = insert(EncoderInformation).values(
            unique_id=new_encoder_info.unique_id,
            encoder_name=new_encoder_info.encoder_name,
            data_source=new_encoder_info.data_source,
            image_trained=new_encoder_info.image_trained,
            total_image_data=new_encoder_info.total_image_data,
            elapsed_encoding_time=new_encoder_info.elapsed_encoding_time,
            should_re_encode=new_encoder_info.should_re_encode,
        )
        await conn.execute(stmt)

    print("New encoder information added successfully.")
    return new_encoder_info.unique_id  # Return the unique_id for further use


async def save_model_details(unique_id: str) -> None:
    # Create a list of mock data for 10 image entries with the same unique_id as the reference
    mock_data = []
    for i in range(10):
        mock_data.append(
            EncoderDetails(
                unique_id=unique_id,  # Use the unique_id from the model information table
                created_at=local_time(),
                updated_at=None,
                image_path=f"/path/to/image_{i}.jpg",  # Mock image path
                image_name=f"image_{i}.jpg",  # Mock image name
                tag_id=f"tag_{i}",
            )
        )

    # Get the database engine
    engine = await database_connection()

    # Insert the new data into the database
    async with engine.begin() as conn:
        # Use execute with an insert statement
        stmt = insert(EncoderDetails).values(
            [
                {
                    "unique_id": detail.unique_id,
                    "created_at": detail.created_at,
                    "updated_at": detail.updated_at,
                    "image_path": detail.image_path,
                    "image_name": detail.image_name,
                    "tag_id": detail.tag_id,
                }
                for detail in mock_data
            ]
        )
        await conn.execute(stmt)

    print("New encoder details added successfully.")


async def main():
    unique_id = await save_model_info()
    await save_model_details(unique_id)


if __name__ == "__main__":
    asyncio.run(main())
