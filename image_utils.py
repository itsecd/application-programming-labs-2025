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


def trim_image_top_left(
    image: Image.Image, 
    target_width: int, 
    target_height: int
) -> Image.Image:
    """
    Обрезает изображение от левого верхнего угла до заданных размеров.
    """

    if target_width <= 0 or target_height <= 0:
        raise ValueError("Ширина и высота должны быть положительными числами")

    original_width, original_height = image.size

    actual_width = min(target_width, original_width)
    actual_height = min(target_height, original_height)

    trimmed_image = image.crop((0, 0, actual_width, actual_height))
    return trimmed_image


def store_image(image: Image.Image, save_path: str) -> None:
    """
    Сохраняет изображение в файл.
    """

    try:
        save_directory = Path(save_path).parent
        if save_directory != Path('.'):
            save_directory.mkdir(parents=True, exist_ok=True)

        image.save(save_path)
    except Exception as e:
        raise IOError(f"Ошибка при сохранении изображения: {e}")