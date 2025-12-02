import numpy as np
import cv2
from typing import Optional, Tuple
import numpy.typing as npt


def add_white_noise(image: npt.NDArray[np.uint8], noise_intensity: float = 25.0) -> npt.NDArray[np.uint8]:
    """
    Накладывает белый шум на изображение
    
    Args:
        image: Входное изображение в формате RGB
        noise_intensity: Интенсивность шума (стандартное отклонение)
    
    Returns:
        Изображение с добавленным шумом
    """
    image_float = image.astype(np.float32)
    noise = np.random.normal(0, noise_intensity, image.shape).astype(np.float32)
    noisy_image = image_float + noise
    noisy_image = np.clip(noisy_image, 0, 255)
    return noisy_image.astype(np.uint8)


def load_image(image_path: str) -> Optional[npt.NDArray[np.uint8]]:
    """
    Загружает изображение и конвертирует в RGB
    
    Args:
        image_path: Путь к изображению
        
    Returns:
        Изображение в формате RGB или None если загрузка не удалась
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_image(image: npt.NDArray[np.uint8], output_path: str) -> bool:
    """
    Сохраняет изображение в формате BGR
    
    Args:
        image: Изображение в формате RGB
        output_path: Путь для сохранения
        
    Returns:
        True если сохранение успешно, False в противном случае
    """
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return cv2.imwrite(output_path, image_bgr)


def get_image_info(image: npt.NDArray[np.uint8]) -> Tuple[int, int, int]:
    """
    Возвращает информацию об изображении
    
    Args:
        image: Входное изображение
        
    Returns:
        Кортеж (высота, ширина, количество каналов)
    """
    height, width, channels = image.shape
    return height, width, channels