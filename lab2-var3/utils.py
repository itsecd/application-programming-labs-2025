from __future__ import annotations
import os
import random
from pathlib import Path
from typing import List, Tuple
from PIL import Image


def cleanup_directory(directory: str) -> None:
    """
    Удаляет из директории все файлы, не являющиеся изображениями.
    """
    if not os.path.exists(directory):
        return

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    for file_path in Path(directory).iterdir():
        if file_path.is_file() and file_path.suffix.lower() not in image_exts:
            try:
                file_path.unlink()
            except Exception:
                pass


def image_matches_size(path: str, min_size: int, max_size: int) -> bool:
    """
    Проверяет, находится ли изображение в заданном диапазоне размеров.
    """
    try:
        with Image.open(path) as img:
            w, h = img.size
            return min_size <= w <= max_size and min_size <= h <= max_size
    except Exception:
        return False


def generate_random_counts(
    size_ranges: List[Tuple[int, int]],
    total_min: int,
    total_max: int
) -> List[int]:
    """
    Генерирует случайное распределение количества изображений по диапазонам,
    суммарно не превышающее заданный максимум.
    """
    num_ranges = len(size_ranges)
    remaining = random.randint(total_min, total_max)
    counts: List[int] = []

    for i in range(num_ranges):
        if i == num_ranges - 1:
            counts.append(remaining)
        else:
            min_count = 1
            max_count = remaining - (num_ranges - i - 1)
            count = random.randint(min_count, max_count)
            remaining -= count
            counts.append(count)

    return counts