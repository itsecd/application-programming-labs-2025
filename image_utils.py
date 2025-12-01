import os
import matplotlib.pyplot as plt
from PIL import Image
from typing import Tuple


def load_image(image_path: str) -> Image.Image:
    """Загружает изображение из файла"""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        raise Exception(f"Ошибка загрузки изображения: {e}")


def get_image_size(image: Image.Image) -> Tuple[int, int]:
    """Возвращает размер изображения"""
    return image.size


def convert_to_pixel_art(image: Image.Image, pixel_size: int = 10) -> Image.Image:
    """
    Преобразует изображение в пиксель-арт

    Args:
        image: Исходное изображение PIL
        pixel_size: Размер пикселя (чем больше, тем более блочным будет результат)

    Returns:
        Преобразованное изображение PIL
    """
    width, height = image.size

    small_width = width // pixel_size
    small_height = height // pixel_size

    small_image = image.resize((small_width, small_height), Image.NEAREST)
    pixel_art = small_image.resize((width, height), Image.NEAREST)

    return pixel_art


def display_images(original: Image.Image, pixel_art: Image.Image) -> None:
    """Отображает исходное и преобразованное изображение"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.imshow(original)
    ax1.set_title("Исходное изображение")
    ax1.axis("off")

    ax2.imshow(pixel_art)
    ax2.set_title("Пиксель-арт")
    ax2.axis("off")

    plt.tight_layout()
    plt.show()


def save_image(image: Image.Image, output_path: str) -> None:
    """Сохраняет изображение в файл"""
    try:
        image.save(output_path)
        print(f"Изображение сохранено: {output_path}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
