import sys
import time
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from celery import Celery
from src.secret import Config
from utils.logger import logging
from utils.helper import local_time
from src.exceptions import NotFoundError

config = Config()

BROKER_URL = f"amqp://{config.RABBITMQ_DEFAULT_USER}:{config.RABBITMQ_DEFAULT_PASS}@{config.RABBITMQ_DEFAULT_HOST}"
RESULT_BACKEND = (
    f"db+postgresql://{config.LOCAL_POSTGRESQL_USER}:"
    f"{config.LOCAL_POSTGRESQL_PASSWORD}@{config.LOCAL_POSTGRESQL_HOST}:"
    f"5432/{config.LOCAL_POSTGRESQL_DATABASE}"
)

app = Celery(
    "testing_celery",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

# Optional: Configure Celery settings
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,  # Task results expire after 1 hour
)


@app.task
def grab_all_images(root_dir: Path) -> list | None:
    """
    Recursively extracting all image path based on root path dir.

    Parameters:
    - root_path: Root directory for searching image data.

    Returns:
    - List of all image data in extension jpg, jpeg, png.
    """
    start_time = local_time()
    if not os.path.exists(path=root_dir):
        raise NotFoundError(
            detail=f"[grab_all_images] Directory {root_dir} not available, make sure its mounted or available in projects directory."
        )

    image_extensions = {".jpg", ".jpeg", ".png"}
    time.sleep(120)
    image_paths = [
        str(path)
        for path in Path(root_dir).rglob("*")
        if path.suffix.lower() in image_extensions
    ]

    if not image_paths:
        raise NotFoundError(
            detail=f"[grab_all_images] No image files found in {root_dir}"
        )
    end_time = local_time()
    logging.info(f"[grab_all_images] Elapsed grab all image: {end_time - start_time}")

    return image_paths
