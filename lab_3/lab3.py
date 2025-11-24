import argparse
import numpy as np
from pathlib import Path
from PIL import Image
import os

def apply_gradient_effect(image, direction='right', intensity=0.5):
    """
    Применяет эффект градиента к изображению.
    
    Args:
        image: Входное изображение (numpy array)
        direction: Направление градиента ('left', 'right', 'top', 'bottom')
        intensity: Интенсивность градиента (0.0 - 1.0)
    
    Returns:
        Изображение с примененным градиентом
    """
 
    result = image.astype(np.float64)
    
    h, w = image.shape[:2]
    gradient = np.linspace(0, intensity, w if direction in ['left', 'right'] else h)
    
    if direction == 'right':
        gradient_mask = np.tile(gradient, (h, 1))
    elif direction == 'left':
        gradient_mask = np.tile(gradient[::-1], (h, 1))
    elif direction == 'bottom':
        gradient_mask = np.tile(gradient, (w, 1)).T
    elif direction == 'top':
        gradient_mask = np.tile(gradient[::-1], (w, 1)).T
    else:
        raise ValueError(f"Неизвестное направление: {direction}")
    
    if len(image.shape) == 3:
        gradient_mask = np.expand_dims(gradient_mask, axis=2)
    
    result += result * gradient_mask
    result = np.clip(result, 0, 255)
    
    return result.astype(np.uint8)

def main():
    parser = argparse.ArgumentParser(description='Применение эффекта градиента к изображению')
    parser.add_argument('--input', type=str, required=True, help='Путь к исходному изображению')
    parser.add_argument('--output', type=str, required=True, help='Путь для сохранения результата')
    parser.add_argument('--direction', type=str, default='right', 
                       choices=['left', 'right', 'top', 'bottom'],
                       help='Направление градиента (default: right)')
    parser.add_argument('--intensity', type=float, default=0.5,
                       help='Интенсивность градиента 0.0-1.0 (default: 0.5)')
    
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Ошибка: Файл {args.input} не найден")
        return
    
    if not 0 <= args.intensity <= 1:
        print("Ошибка: Интенсивность должна быть между 0.0 и 1.0")
        return
    
    try:
        pil_image = Image.open(args.input)
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        image = np.array(pil_image)
    except Exception as e:
        print(f"Ошибка: Не удалось загрузить изображение из {args.input}: {e}")
        return
    
    print(f"Размер изображения: {image.shape}")
    print(f"Тип данных: {image.dtype}")
    
    result_image = apply_gradient_effect(image, args.direction, args.intensity)
    
    try:
        result_pil = Image.fromarray(result_image)
        result_pil.save(args.output)
        print(f"Успешно: Результат сохранен в {args.output}")
        print(f"Эффект градиента применен в направлении: {args.direction}")
        print(f"Интенсивность эффекта: {args.intensity}")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")

if __name__ == "__main__":
    main()