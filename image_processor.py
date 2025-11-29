# image_processor.py
import cv2
import numpy as np
import os

def calculate_average_brightness(file_path: str) -> tuple:
    """
    Расчёт средней яркости для каждого канала (R, G, B)
    :param file_path: Путь к файлу изображения
    :return: Кортеж из средних значений яркости каждого канала
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Ошибка: Файл не найден по пути {file_path}")

    img = cv2.imread(file_path)

    b_channel, g_channel, r_channel = cv2.split(img)

    avg_r = np.mean(r_channel)
    avg_g = np.mean(g_channel)
    avg_b = np.mean(b_channel)

    return avg_r, avg_g, avg_b