import os

import cv2
import numpy as np


def read_image(image_path: str) -> np.ndarray:
    """
    Reads image by path and returns it as an array.
    :param image_path: Filepath to the image to be read.
    :return: Image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Error while reading file, path: {image_path}")

    return image


def save_image(image_path: str, image: np.ndarray) -> None:
    """
    Save image by path.
    :param image_path: Path where to save image.
    :param image: Image to save.
    """
    try:
        directory = os.path.dirname(image_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        cv2.imwrite(image_path, image)
    except Exception as e:
        raise IOError(f"Could not save image to: {image_path}. Reason: {e}")
