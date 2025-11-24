from pathlib import Path
from typing import Tuple
from PIL import Image


def open_image(file_path: str) -> Image.Image:
    """
    Загружает изображение из файла.
    """

    if not Path(file_path).exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        image = Image.open(file_path)
        return image
    except Exception as e:
        raise IOError(f"Ошибка при загрузке изображения: {e}")


def get_dimensions(image: Image.Image) -> Tuple[int, int]:
    """
    Получает размер изображения.
    """
    
    return image.size