import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Tuple

def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Изменение размера изображения')
    parser.add_argument('--input', '-i', required=True, help='Путь к исходному изображению')
    parser.add_argument('--output', '-o', required=True, help='Путь для сохранения результата')
    parser.add_argument('--width', '-w', type=int, required=True, help='Новая ширина изображения')
    parser.add_argument('--height', '-ht', type=int, required=True, help='Новая высота изображения')
    return parser.parse_args()

def load_image(path) -> np.ndarray:
    """Загрузка изображения с проверкой"""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Не удалось загрузить изображение: {path}")
    return img

def resize_image(image, width, height) -> np.ndarray:
    """Изменение размера изображения"""
    return cv2.resize(image, (width, height))

def create_comparison_plot(original_img, resized_img, original_size, new_size) -> None:
    """Создание сравнительного графика"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    ax1.set_title(f'Исходное изображение\n({original_size[0]}x{original_size[1]})')
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'Измененное изображение\n({new_size[0]}x{new_size[1]})')
    ax2.axis('off')

    plt.tight_layout()
    plt.show()

def save_image(image, output_path) -> None:
    """Сохранение изображения с созданием директорий при необходимости"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)

def main() -> None:
    args = parse_arguments()
    
    original_img = load_image(args.input)
    original_size = (original_img.shape[1], original_img.shape[0])
    print(f"Размер исходного изображения: {original_size[0]}x{original_size[1]}")
    
    resized_img = resize_image(original_img, args.width, args.height)
    
    create_comparison_plot(original_img, resized_img, original_size, (args.width, args.height))
    
    save_image(resized_img, args.output)
    print(f"Результат сохранен в: {args.output}")

if __name__ == "__main__":
    main()