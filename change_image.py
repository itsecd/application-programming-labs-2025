import cv2
import numpy as np


def bgr_2_rgb(img: np.ndarray) -> np.ndarray:
    """
    Конвертирование изображения для корректного отображения
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def change_image(image_rgb: np.ndarray) -> np.ndarray:
    """
    Изменение изображения
    """
    image_changed = image_rgb[:, :, [2, 1, 0]]
    return image_changed
