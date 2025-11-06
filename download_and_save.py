import os

import cv2
import numpy as np


def download_image(filenamepath_image: str) -> np.ndarray:
    """
    Считывание изображения
    """
    if os.path.exists(filenamepath_image):
        img = cv2.imread(filenamepath_image)
        shape = img.shape
        print(shape)
        return img


def save_image(filename_save: str, img_changed: np.ndarray) -> None:
    """
    Сохранение изображения
    """
    if not os.path.exists(filename_save):
        os.mkdir(filename_save)
    output_path = os.path.join(filename_save, "output.jpg")
    cv2.imwrite(output_path, cv2.cvtColor(img_changed, cv2.COLOR_BGR2RGB))
