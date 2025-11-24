import os
import time
from pathlib import Path
from typing import Tuple

from PIL import Image


def filter_by_resolution(folder: str,
                         min_res: Tuple[int, int],
                         max_res: Tuple[int, int]) -> int:
    """
    Фильтрует изображения по разрешению.
    Возвращает количество оставшихся изображений.
    """

    allowed_ext = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    time.sleep(0.8)  # Задержка для избежания проблем с файловой системой

    files = [
        f for f in os.listdir(folder)
        if Path(f).suffix.lower() in allowed_ext
    ]

    kept, removed = 0, 0
    for name in files:
        path = os.path.join(folder, name)

        try:
            with Image.open(path) as img:
                w, h = img.size

            if not (min_res[0] <= w <= max_res[0] and min_res[1] <= h <= max_res[1]):
                os.remove(path)
                removed += 1
            else:
                kept += 1

        except Exception:
            try:
                os.remove(path)
                removed += 1
            except Exception:
                pass

    return kept