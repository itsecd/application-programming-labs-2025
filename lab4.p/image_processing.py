from __future__ import annotations
from pathlib import Path
from typing import Literal

import numpy as np
from PIL import Image
import pandas as pd

Orientation = Literal["Horizontal", "Vertical", "Square"]


def add_orientation_column(
    df: pd.DataFrame,
    abs_col: str = "absolute_path",
    new_col: str = "orientation",
) -> pd.DataFrame:
    """Добавить колонку ориентации изображения по absolute_path."""
    df_new = df.copy()
    values: list[Orientation | None] = []

    for p in df_new[abs_col]:
        path = Path(str(p))

        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                arr = np.array(img)
        except Exception as e:
            print("Не удалось открыть файл:", path, "| ошибка:", e)
            values.append(None)
            continue

        h, w = arr.shape[:2]

        if w > h:
            values.append("Horizontal")
        elif h > w:
            values.append("Vertical")
        else:
            values.append("Square")

    df_new[new_col] = values
    return df_new


def sort_by_orientation(df: pd.DataFrame, col: str = "orientation") -> pd.DataFrame:
    """Отсортировать по ориентации."""
    return df.sort_values(by=col)


def filter_by_orientation(
    df: pd.DataFrame, orientation: Orientation, col: str = "orientation"
) -> pd.DataFrame:
    """Отфильтровать по ориентации."""
    return df[df[col] == orientation].copy()
