import cv2
import numpy as np


def read_image(path: str) -> np.ndarray:
    """
    Считывание изображения
    :param path: путь к файлу
    :return: многомерный массив пикселей
    """
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # возможно 1,3 или 4 канала
    return img

def give_image_info(img: np.ndarray) -> tuple:
    """
    Получение информации об изображении
    :param img: многомерный массив пикселей
    :return: образ изображения
    """
    # img.shape: (h, w) или (h, w, c)
    shape = img.shape
    return shape

def save_image(path: str, img: np.ndarray) -> None:
    """
    Сохранение изображения
    :param path: путь для сохранения изображения
    :param img: многомерных массив пикселей полутонового изображения
    """
    if img.dtype != np.uint8:
        if np.issubdtype(img.dtype, np.floating):
            img_to_save = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        else:
            img_to_save = img.astype(np.uint8)
    else:
        img_to_save = img

    cv2.imwrite(path, img_to_save)