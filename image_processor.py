from PIL import Image
import numpy as np


def calculate_brightness_range(image_path: str) -> float | None:
    """Вычисляет диапазон яркости изображения (max-min) по всем каналам."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        brightness_range = img_array.max() - img_array.min()
        return brightness_range
    except Exception as e:
        return None