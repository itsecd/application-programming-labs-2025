import argparse
from typing import Optional

import cv2
import numpy as np
from image_processor import create_puzzle
from visualizer import show_comparison


def load_image_alternative(image_path: str) -> Optional[np.ndarray]:
    """Альтернативный способ загрузки изображения(из-за проблем с кодировкой)"""
    try:
        img = cv2.imread(image_path)
        if img is not None:
            return img
        
        with open(image_path, 'rb') as f:
            file_bytes = np.frombuffer(f.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            return img
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description='Создание паззла из изображения')
    parser.add_argument('input', help='Путь к исходному изображению')
    parser.add_argument('output', help='Путь для сохранения паззла')
    parser.add_argument('n', type=int, help='Количество частей по горизонтали и вертикали')
    
    args = parser.parse_args()
    
    try:
        original_img = load_image_alternative(args.input)
        if original_img is None:
            print(f"Не удалось загрузить изображение: {args.input}")
            return
        
        print(f"Изображение успешно загружено, размер: {original_img.shape}")
        
        original_img, puzzle_img = create_puzzle(original_img, args.n)
        
        success = cv2.imwrite(args.output, puzzle_img)
        if success:
            print(f"Паззл успешно сохранен в: {args.output}")
        else:
            print(f"Ошибка сохранения в: {args.output}")
        
        show_comparison(original_img, puzzle_img, args.n)
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()