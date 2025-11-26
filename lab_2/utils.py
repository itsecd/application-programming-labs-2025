import os
from pathlib import Path
from typing import List, Tuple

def validate_and_create_dir(path: str) -> Path:
    """
    Проверяет существование директории и создает её при необходимости.

    Args:
        path (str): Путь к директории.

    Returns:
        Path: Объект Path к созданной/существующей директории.

    Raises:
        ValueError: Если путь не является директорией или не может быть создан.
    """
    dir_path = Path(path).resolve()
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Не удалось создать директорию {dir_path}: {e}")
    return dir_path

def get_image_paths(directory: Path) -> List[Path]:
    """
    Получает список путей к изображениям в директории.

    Args:
        directory (Path): Директория для поиска изображений.

    Returns:
        List[Path]: Список путей к изображениям.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    return [
        file for file in directory.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    ]

def calculate_per_keyword_count(total_images: int, keywords: List[str]) -> int:
    """
    Рассчитывает количество изображений на каждое ключевое слово.

    Args:
        total_images (int): Общее количество изображений.
        keywords (List[str]): Список ключевых слов.

    Returns:
        int: Количество изображений на одно ключевое слово.

    Raises:
        ValueError: Если количество ключевых слов равно нулю.
    """
    if len(keywords) == 0:
        raise ValueError("Список ключевых слов не может быть пустым")
    per_keyword = total_images // len(keywords)
    if per_keyword == 0:
        raise ValueError("Общее количество изображений слишком мало для заданного числа ключевых слов")
    return per_keyword