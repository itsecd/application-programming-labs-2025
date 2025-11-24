import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def parse_arguments():
    """
    парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='преобразование изображения в бинарное')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='путь к исходному изображению')
    parser.add_argument('-o', '--output', type=str,
                        help='путь для сохранения изображения (опционально)')
    parser.add_argument('-th', '--threshold', type=int, default=127,
                        help='порог для бинаризации')


    return parser.parse_args()


def validate_arguments(input_path: str, threshold: int) -> None:
    """
    проверка корректности аргументов
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"файл не найден: {input_path}")

    if not 0 <= threshold <= 255:
        raise ValueError("порог должен быть в диапазоне от 0 до 255")


def load_image(image_path: str) -> np.ndarray:
    """
    загрузка изображения
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"не удалось загрузить изображение: {image_path}")
    return img


def binarize_image(img: np.ndarray, threshold: int) -> np.ndarray:
    """
    бинаризация
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary


def save_image(image: np.ndarray, output_path: str) -> None:
    """
    сохранение результатов
    """
    if os.path.exists(output_path):
        raise FileExistsError(f"файл уже существует: {output_path}")

    if not cv2.imwrite(output_path, image):
        raise ValueError(f"ошибка при сохранении изображения: {output_path}")
