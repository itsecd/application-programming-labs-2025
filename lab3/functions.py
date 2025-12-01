import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_pixel_art(image: np.ndarray, pixel_size: int = 10) -> np.ndarray:
    """Преобразует изображение в пиксель-арт.
    
    Args:
        image: Входное изображение в формате numpy array.
        pixel_size: Размер одного пикселя в пиксель-арте.
        
    Returns:
        np.ndarray: Изображение в стиле пиксель-арт.
        
    Raises:
        Exception: Если возникает ошибка при обработке изображения.
    """
    
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
    """Читает изображение с диска.
    
    Args:
        image_path: Путь к файлу изображения.
        
    Returns:
        np.ndarray: Загруженное изображение.
        
    Raises:
        Exception: Если изображение не найдено или не может быть загружено.
    """
   
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение {image_path}")
        return img
    except Exception as e:
        raise Exception(f"Ошибка в read_image: {e}")

def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """Конвертирует изображение из BGR в RGB формат.
    
    Args:
        image: Изображение в формате BGR.
        
    Returns:
        np.ndarray: Изображение в формате RGB.
        
    Raises:
        Exception: Если возникает ошибка при конвертации.
    """
    
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise Exception(f"Ошибка в convert_bgr_to_rgb: {e}")

def convert_rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """Конвертирует изображение из RGB в BGR формат.
    
    Args:
        image: Изображение в формате RGB.
        
    Returns:
        np.ndarray: Изображение в формате BGR.
        
    Raises:
        Exception: Если возникает ошибка при конвертации.
    """
    
    try:
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise Exception(f"Ошибка в convert_rgb_to_bgr: {e}")

def save_image(image: np.ndarray, output_path: str) -> None:
    """Сохраняет изображение на диск.
    
    Args:
        image: Изображение для сохранения.
        output_path: Путь для сохранения файла.
        
    Raises:
        Exception: Если возникает ошибка при сохранении.
    """
    
    try:
        cv2.imwrite(output_path, image)
    except Exception as e:
        raise Exception(f"Ошибка в save_image: {e}")

def display_images(original: np.ndarray, pixel_art: np.ndarray, pixel_size: int) -> None:
    """Отображает исходное изображение и результат пиксель-арта.
    
    Args:
        original: Исходное изображение.
        pixel_art: Результат пиксель-арта.
        pixel_size: Размер пикселя, использованный для преобразования.
    """
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title('Исходное изображение')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(pixel_art)
    plt.title(f'Пиксель-арт (размер пикселя: {pixel_size})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
