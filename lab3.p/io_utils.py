from __future__ import annotations

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


class ImageReadError(Exception):
    """Ошибка чтения изображения."""
    pass


def read_image(path: str | Path) -> np.ndarray:
    """Читает изображение BGR из файла."""
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise ImageReadError(f"Файл не найден: {p}")
    img = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if img is None:
        raise ImageReadError(f"Не удалось загрузить: {p}")
    return img


def save_image(path: str | Path, image: np.ndarray) -> None:
    """Сохраняет изображение на диск."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(p), image):
        raise IOError(f"Не удалось сохранить: {p}")


def image_size(image: np.ndarray) -> Tuple[int, int]:
    """Возвращает (width, height)."""
    h, w = image.shape[:2]
    return w, h