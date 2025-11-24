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

def stitch_images(image1, image2, direction='horizontal'):
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    if direction == 'horizontal':
        if h1 != h2:
            min_height = min(h1, h2)
            image1_resized = np.array(Image.fromarray(image1).resize((w1, min_height)))
            image2_resized = np.array(Image.fromarray(image2).resize((w2, min_height)))
            result = np.hstack((image1_resized, image2_resized))
        else:
            result = np.hstack((image1, image2))
            
    elif direction == 'vertical':
        if w1 != w2:
            min_width = min(w1, w2)
            image1_resized = np.array(Image.fromarray(image1).resize((min_width, h1)))
            image2_resized = np.array(Image.fromarray(image2).resize((min_width, h2)))
            result = np.vstack((image1_resized, image2_resized))
        else:
            result = np.vstack((image1, image2))
    
    return result

def save_image(image, output_path):
    Image.fromarray(image).save(output_path)
    print(f"Результат сохранен в: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Соединение двух изображений')
    parser.add_argument('image1', type=str, help='Путь к первому изображению')
    parser.add_argument('image2', type=str, help='Путь ко второму изображению')
    parser.add_argument('--output', type=str, default='stitched_result.jpg')
    parser.add_argument('--direction', type=str, choices=['horizontal', 'vertical'], default='horizontal')
    
    args = parser.parse_args()
    
    try:
        print("Загрузка изображений...")
        image1 = load_image(args.image1)
        image2 = load_image(args.image2)
        
        print(f"Изображение 1: {image1.shape[1]}x{image1.shape[0]}")
        print(f"Изображение 2: {image2.shape[1]}x{image2.shape[0]}")
        
        print(f"Соединение изображений ({args.direction})...")
        result = stitch_images(image1, image2, args.direction)
        
        print(f"Результат: {result.shape[1]}x{result.shape[0]}")
        
        print("Сохранение результата...")
        save_image(result, args.output)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()