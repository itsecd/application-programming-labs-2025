from __future__ import annotations
import os
from typing import Tuple
import cv2
import numpy as np
from numpy.typing import NDArray


def load_image(path: str) -> NDArray[np.uint8]:
    """Загружает изображение и возвращает его в формате RGB.

    Args:
        path (str): Путь к файлу изображения.

    Returns:
        NDArray[np.uint8]: Изображение в формате RGB (H×W×3).
    """
    if not os.path.exists(path):
        raise FileNotFoundError

    img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError

    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def save_image(image_rgb: NDArray[np.uint8], path: str) -> None:
    """Сохраняет изображение в формате, понятном OpenCV (BGR).

    Args:
        image_rgb (NDArray[np.uint8]): Изображение в формате RGB.
        path (str): Путь, куда сохранить файл (с расширением).
    """
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    success = cv2.imwrite(path, image_bgr)
    if not success:
        raise OSError