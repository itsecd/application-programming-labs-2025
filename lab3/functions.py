import cv2
import numpy as np
from typing import Tuple

def create_pixel_art(image: np.ndarray, pixel_size: int = 10) -> np.ndarray:
    
    try:
        # Получаем размеры исходного изображения
        height, width = image.shape[:2]
        
        # Уменьшаем изображение
        small_width = width // pixel_size
        small_height = height // pixel_size
        
        # Уменьшаем изображение до маленького размера
        small_image = cv2.resize(image, (small_width, small_height), interpolation=cv2.INTER_NEAREST)
        
        # Увеличиваем обратно до исходного размера
        pixel_art = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)
        
        return pixel_art
    except Exception as e:
        raise Exception(f"Ошибка в create_pixel_art: {e}")

def read_image(image_path: str) -> np.ndarray:
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение {image_path}")
        return img
    except Exception as e:
        raise Exception(f"Ошибка в read_image: {e}")

def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise Exception(f"Ошибка в convert_bgr_to_rgb: {e}")

def convert_rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    
    try:
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise Exception(f"Ошибка в convert_rgb_to_bgr: {e}")

def save_image(image: np.ndarray, output_path: str) -> None:
    
    try:
        cv2.imwrite(output_path, image)
    except Exception as e:
        raise Exception(f"Ошибка в save_image: {e}")