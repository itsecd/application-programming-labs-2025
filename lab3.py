import argparse
import os
from PIL import Image
import numpy as np

def load_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл {image_path} не найден")
    image = Image.open(image_path)
    image_array = np.array(image)
    return image_array

def save_image(image, output_path):
    Image.fromarray(image).save(output_path)
    print(f"Результат сохранен в: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Обработка изображений')
    parser.add_argument('image1', type=str, help='Путь к первому изображению')
    parser.add_argument('image2', type=str, help='Путь ко второму изображению')
    parser.add_argument('--output', type=str, default='result.jpg')
    
    args = parser.parse_args()
    
    try:
        print("Загрузка изображений...")
        image1 = load_image(args.image1)
        image2 = load_image(args.image2)
        
        print(f"Изображение 1: {image1.shape[1]}x{image1.shape[0]}")
        print(f"Изображение 2: {image2.shape[1]}x{image2.shape[0]}")
        
        result = image1
        
        print("Сохранение результата...")
        save_image(result, args.output)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()