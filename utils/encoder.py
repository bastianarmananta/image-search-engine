import os
import numpy as np
from torch import Tensor
from pathlib import Path
from PIL import Image, ImageOps
from utils.logger import logging
from utils.helper import local_time
from src.exceptions import NotFoundError
from sentence_transformers import SentenceTransformer
from sentence_transformers.SentenceTransformer import SentenceTransformer as model_type


def init_model(model: str = "clip-ViT-B-32") -> SentenceTransformer:
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
    logging.info(f"[init_model] Elapsed loading model: {end_time-start_time}")

    return model


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

    logging.info("[grab_all_images] Start finding image data.")
    image_extensions = {".jpg", ".jpeg", ".png"}
    image_paths = [
        str(path)
        for path in Path(root_dir).rglob("*")
        if path.suffix.lower() in image_extensions
    ]
    logging.info("[grab_all_images] Finished find all image data.")
    logging.info(
        f"[grab_all_images] Found total {len(image_paths)} image on {root_dir}."
    )

    if not image_paths:
        raise NotFoundError(
            detail=f"[grab_all_images] No image files found in {root_dir}"
        )

    end_time = local_time()

    logging.info(
        f"[grab_all_images] Elapsed retrive all image data: {end_time-start_time}"
    )

    return image_paths


def preprocess_images(images: list) -> list:
    """
    Preprocess images by resizing, grayscale, normalizing etc.
    Parameters:
    - images: List of image paths.

    Returns:
    - List of preprocessed images using ImageOps.
    """

    start_time = local_time()
    logging.info("[preprocess_images] Starting preprocessing data.")

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

    processed_images = [process_image(image_path=image) for image in images]
    end_time = local_time()
    logging.info("[preprocess_images] Finished preprocessing data.")
    logging.info(
        f"[preprocess_images] Elapsed preprocessing data {end_time-start_time}"
    )

    return processed_images


def validate_directory(directory_name: str = "cache") -> str:
    if not os.path.exists(path=directory_name):
        logging.info(f"[validate_directory] Creating {directory_name} dir.")
        os.makedirs(name="cache", exist_ok=True)

    logging.info(
        f"[validate_directory] Skip creating. {directory_name} dir already created."
    )

    return directory_name


def save_encoded_images(
    root_dir: Path, encoded_name: str, encoded_data: Tensor
) -> None:
    cache_file = f"{root_dir}/{encoded_name}.npy"
    np.save(cache_file, encoded_data.cpu().numpy())
    logging.info(
        f"[save_encoded_images] Saved new encoding file {os.path.join(root_dir, encoded_name)}."
    )


def encode_images(
    preprocessed_image: list, model: model_type, encoded_name: str, batch_size: int = 4
) -> None:
    logging.info("[encode_images] Starting encoding.")
    cache_dir = validate_directory()
    encode_images = model.encode(
        sentences=preprocessed_image,
        batch_size=batch_size,
        convert_to_tensor=True,
        show_progress_bar=True,
    )
    logging.info("[encode_images] Encoding finished.")
    save_encoded_images(
        root_dir=cache_dir, encoded_name=encoded_name, encoded_data=encode_images
    )
    logging.info(f"[encode_images] Encoder {encoded_name} saved.")
