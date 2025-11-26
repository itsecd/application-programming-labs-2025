import argparse
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
# python3 lab3.py ./000001.jpg output.jpg
def load_image(image_path):
    """Загружает изображение из файла"""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return None

def get_image_size(image):
    """Возвращает размер изображения"""
    return image.size

def convert_to_pixel_art(image, pixel_size=10):
    """
    Преобразует изображение в пиксель-арт
    
    Args:
        image: Исходное изображение PIL
        pixel_size: Размер пикселя (чем больше, тем более блочным будет результат)
    
    Returns:
        Преобразованное изображение PIL
    """
    width, height = image.size
    
    
    small_width = width // pixel_size
    small_height = height // pixel_size
    
    small_image = image.resize((small_width, small_height), Image.NEAREST)
    
    # обратно
    pixel_art = small_image.resize((width, height), Image.NEAREST)
    
    return pixel_art

def display_images(original, pixel_art):
    """Отображает исходное и преобразованное изображение"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.imshow(original)
    ax1.set_title('Исходное изображение')
    ax1.axis('off')
    
    ax2.imshow(pixel_art)
    ax2.set_title('Пиксель-арт')
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

def save_image(image, output_path):
    """Сохраняет изображение в файл"""
    try:
        image.save(output_path)
        print(f"Изображение сохранено: {output_path}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def main():
    """Основная функция"""
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Преобразование изображения в пиксель-арт')
    parser.add_argument('input_path', help='Путь к исходному изображению')
    parser.add_argument('output_path', help='Путь для сохранения результата')
    parser.add_argument('--pixel_size', type=int, default=10, 
                       help='Размер пикселя (по умолчанию: 10)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"Ошибка: файл {args.input_path} не существует")
        return
    
    print("Загрузка изображения")
    original_image = load_image(args.input_path)
    if original_image is None:
        return
    
    width, height = get_image_size(original_image)
    print(f"Размер изображения: {width}x{height} пикселей")
    
    print(f"Преобразование в пиксель-арт (размер пикселя: {args.pixel_size})")
    pixel_art_image = convert_to_pixel_art(original_image, args.pixel_size)
    
    save_image(pixel_art_image, args.output_path)
    
    print("Отображение результатов...")
    display_images(original_image, pixel_art_image)
    
    print("Готово!")

if __name__ == "__main__":
    main()