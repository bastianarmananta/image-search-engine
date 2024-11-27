import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from petname import generate
from datetime import timedelta
from utils.logger import logging
from utils.helper import local_time
from services.celery.worker import app
from utils.encoder import init_model, preprocess_images, grab_all_images, encode_images


@app.task
def start_encoder_task(root_path: Path) -> None:
    start_time = local_time()
    model_name = generate()
    initialize_model = init_model()
    images = grab_all_images(root_dir=root_path)
    preprocessed_images = preprocess_images(images=images)
    encode_images(
        preprocessed_image=preprocessed_images,
        model=initialize_model,
        encoded_name=model_name,
    )
    end_time = local_time()
    elapsed_time = end_time - start_time
    formatted_time = str(timedelta(seconds=elapsed_time.total_seconds()))
    logging.info(f"Elapsed encoder task: {formatted_time}")
