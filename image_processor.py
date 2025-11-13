import numpy as np
from PIL import Image


def calculate_brightness_range(image_path):
    """Вычисляет диапазон яркости изображения (max-min) по всем каналам."""
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        brightness_range = img_array.max() - img_array.min()
        return brightness_range
    except Exception as e:
        print(f"Ошибка при обработке {image_path}: {e}")
        return None