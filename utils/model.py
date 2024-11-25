import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from torch import Tensor
from PIL import Image, ImageOps
from utils.logger import logging
from utils.helper import local_time
from sentence_transformers import SentenceTransformer
from sentence_transformers.SentenceTransformer import SentenceTransformer as model_type


async def init_model(
    model: str = "clip-ViT-B-32",
) -> SentenceTransformer:
    """
    Load Visual Transformers model.
    This uses the CLIP model for encoding.

    |   Model 	        |   Top 1 Performance   |
    |   clip-ViT-B-32 	|   63.3                |
    |   clip-ViT-B-16 	|   68.1                |
    |   clip-ViT-L-14 	|   75.4                |
    """
    start_time = local_time()
    model = SentenceTransformer(model_name_or_path=model)
    end_time = local_time()
    logging.info(
        f"[init_model] Elapsed model initialization process: {end_time-start_time}"
    )
    return model


async def preprocess_images(images: list) -> list:
    """
    Preprocess images by resizing, grayscale, normalizing etc.
    Parameters:
    - images: List of image paths.

    Returns:
    - List of preprocessed images using ImageOps.
    """

    def process_image(image_path: str) -> Image:
        """Process each image and return the preprocessed image."""
        image_data = Image.open(image_path)
        image = ImageOps.fit(image_data, (224, 224))
        image = ImageOps.grayscale(image)
        image = ImageOps.autocontrast(image)
        image = ImageOps.flip(image)
        image = ImageOps.expand(image)
        image = ImageOps.mirror(image)
        return image

    start_time = local_time()
    processed_images = await asyncio.gather(
        *(asyncio.to_thread(process_image, image) for image in images)
    )
    end_time = local_time()
    logging.info(
        f"[preprocess_images] Elapsed encoding data process: {end_time - start_time}"
    )

    return processed_images


async def encode_images(
    preprocessed_image: list, model: model_type, cache_name: str, batch_size: int = 4
) -> Tensor:
    pass
