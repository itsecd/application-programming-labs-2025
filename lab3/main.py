import argparse
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Поворот изображения на заданный угол."
    )

    parser.add_argument("path_in", type=str, help="Путь к исходному изображению")
    parser.add_argument("path_out", type=str, help="Путь для сохранения результата")
    parser.add_argument("angle", type=float, help="Угол поворота изображения")

    return parser.parse_args()


def load_image(path: str) -> np.ndarray:
    """
    загружает изображение из файла
    """
    pass


def print_image_info(image: np.ndarray) -> None:
    """
    выводит информацию о размере загруженного изображения
    """
    pass


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """
    поворачивает изображение на заданный угол
    """
    pass


def show_before_after(original: np.ndarray, transformed: np.ndarray) -> None:
    """
    отображает исходное и преобразованное изображение рядом
    """
    pass


def save_image(path: str, image: np.ndarray) -> None:
    """
    сохраняет изображение в файл
    """
    pass


def main():
    try:
        args = parse_arguments()

        image = load_image(args.path_in)

        print_image_info(image)
        rotated = rotate_image(image, args.angle)

        show_before_after(image, rotated)

        save_image(args.path_out, rotated)

    except Exception as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
