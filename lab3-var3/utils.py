import cv2
import numpy as np
from typing import Tuple

def resize_by_height(img: np.ndarray, height: int) -> np.ndarray:
    """Изменяет размер изображения по высоте с сохранением пропорций."""
    return cv2.resize(img, (int(img.shape[1] * height / img.shape[0]), height))

def resize_by_width(img: np.ndarray, width: int) -> np.ndarray:
    """Изменяет размер изображения по ширине с сохранением пропорций."""
    return cv2.resize(img, (width, int(img.shape[0] * width / img.shape[1])))

def ensure_3_channels(img: np.ndarray) -> np.ndarray:
    """Преобразует изображение в 3-канальное (BGR)."""
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        img = img[:, :, :3]
    return img

def concatenate_images(img1: np.ndarray, img2: np.ndarray, axis: str = "horizontal") -> np.ndarray:
    """Соединяет два изображения по горизонтали или вертикали с подгонкой размеров."""
    if axis == "horizontal":
        height = min(img1.shape[0], img2.shape[0])
        img1_resized = resize_by_height(img1, height)
        img2_resized = resize_by_height(img2, height)
        return np.hstack((img1_resized, img2_resized))
    else:
        width = min(img1.shape[1], img2.shape[1])
        img1_resized = resize_by_width(img1, width)
        img2_resized = resize_by_width(img2, width)
        return np.vstack((img1_resized, img2_resized))