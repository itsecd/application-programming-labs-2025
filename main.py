import argparse
import cv2
import os
import numpy as np
from image_processor import create_puzzle
from visualizer import show_comparison

def main():
    parser = argparse.ArgumentParser(description='Создание паззла из изображения')
    parser.add_argument('input', help='Путь к исходному изображению')
    parser.add_argument('output', help='Путь для сохранения паззла')
    parser.add_argument('n', type=int, help='Количество частей по горизонтали и вертикали')
    
    args = parser.parse_args()
    
    try:
        original_img, puzzle_img = create_puzzle(args.input, args.n)
        print(f"Размер изображения: {original_img.shape}")
        output_path = "puzzle_result.jpg"
        success = save_image_alternative(output_path, puzzle_img)
        if success:
            print(f"Паззл успешно сохранен в: {output_path}")
        else:
            print("Ошибка сохранения")
        
        show_comparison(original_img, puzzle_img, args.n)
        
    except Exception as e:
        print(f"Ошибка: {e}")

def save_image_alternative(image_path, image):
    """Альтернативный способ сохранения изображения(из-за проблем с кодировкой)"""
    try:
        """Сохраняет в текущую папку"""
        success = cv2.imwrite(image_path, image)
        if success:
            return True
        
        """Если не получилось, пробуем через imencode"""
        extension = os.path.splitext(image_path)[1]
        success, encoded_image = cv2.imencode(extension, image)
        if success:
            with open(image_path, 'wb') as f:
                f.write(encoded_image.tobytes())
            return True
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
    
    return False

if __name__ == "__main__":
    main()