from __future__ import annotations
from pathlib import Path
from typing import Tuple
from PIL import Image

def get_image_dimensions(image_path: str | Path) -> Tuple[int, int]:
    """Открывает изображение и возвращает его размеры.

    Args:
        image_path (str | Path): Путь к файлу изображения.

    Returns:
        Tuple[int, int]: (ширина, высота) в пикселях.
                         Возвращает (0, 0) при любой ошибке открытия.
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as exc:
        print(f"[Ошибка] Не удалось открыть {image_path}: {exc}")
        return 0, 0