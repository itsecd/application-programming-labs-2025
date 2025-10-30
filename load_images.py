import os

import cv2
import numpy as np


def load_images(folder: str) -> list[np.ndarray]:
    """
    функция для скачивания изображения и сохранение ее в массив
    """
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")
            ):
                file_path = os.path.join(root, file)
                img = cv2.imread(file_path)
                images.append(img)
    return images
