from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional
from utils import get_image_dimensions

def create_dataframe_from_folder(folder_path: str | Path) -> pd.DataFrame:
    """Создаёт DataFrame со всеми изображениями из указанной папки.

    Args:
        folder_path (str | Path): Путь к папке с изображениями.

    Returns:
        pd.DataFrame: Таблица с колонками:
            - filename
            - absolute_path
            - relative_path
            - width_px
            - height_px
            - aspect_ratio (width / height, округлено до 4 знаков)

    Raises:
        NotADirectoryError: Если указанный путь не является папкой.
    """
    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Папка не найдена: {folder}")

    extensions = {
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff',
        '.webp', '.gif', '.heic', '.avif'
    }

    records = []
    for file_path in folder.iterdir():
        if file_path.suffix.lower() in extensions and file_path.is_file():
            width, height = get_image_dimensions(file_path)
            if width == 0 or height == 0:
                continue

            aspect_ratio = round(width / height, 4)

            records.append({
                'filename': file_path.name,
                'absolute_path': str(file_path.absolute()),
                'relative_path': str(file_path.relative_to(Path.cwd())),
                'width_px': width,
                'height_px': height,
                'aspect_ratio': aspect_ratio
            })

    return pd.DataFrame(records)


def create_dataframe_from_csv(csv_path: str | Path) -> pd.DataFrame:
    """Загружает готовый анализ из CSV-файла.

    Args:
        csv_path (str | Path): Путь к CSV-файлу.

    Returns:
        pd.DataFrame: Загруженная таблица.
    """
    return pd.read_csv(csv_path)


def sort_by_aspect_ratio(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    """Сортирует DataFrame по отношению сторон.

    Args:
        df (pd.DataFrame): Исходный DataFrame.
        ascending (bool): True — по возрастанию, False — по убыванию.

    Returns:
        pd.DataFrame: Отсортированный DataFrame с новым индексом.
    """
    return df.sort_values(by='aspect_ratio', ascending=ascending).reset_index(drop=True)


def filter_by_aspect_ratio(
    df: pd.DataFrame,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None
) -> pd.DataFrame:
    """Фильтрует изображения по диапазону отношения сторон.

    Args:
        df (pd.DataFrame): Исходный DataFrame.
        min_ratio (float | None): Минимальное значение aspect_ratio (включительно).
        max_ratio (float | None): Максимальное значение aspect_ratio (включительно).

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame.
    """
    result = df.copy()
    if min_ratio is not None:
        result = result[result['aspect_ratio'] >= min_ratio]
    if max_ratio is not None:
        result = result[result['aspect_ratio'] <= max_ratio]
    return result.reset_index(drop=True)