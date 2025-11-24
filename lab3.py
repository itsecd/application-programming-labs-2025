import argparse
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def create_test_images():
    if not os.path.exists('photo1.png'):
        img1 = np.zeros((300, 400, 3), dtype=np.uint8)
        for i in range(400):
            img1[:, i] = [100, 100, 255 - i//2]
        Image.fromarray(img1).save('photo1.png')
        print("Создано тестовое изображение: photo1.png")
    
    if not os.path.exists('photo2.png'):
        img2 = np.zeros((300, 400, 3), dtype=np.uint8)
        for i in range(400):
            img2[:, i] = [255 - i//2, 100, 100]
        Image.fromarray(img2).save('photo2.png')
        print("Создано тестовое изображение: photo2.png")

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

def display_images(original1, original2, result):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(original1)
    axes[0].set_title(f'Изображение 1\n{original1.shape[1]}x{original1.shape[0]}')
    axes[0].axis('off')
    
    axes[1].imshow(original2)
    axes[1].set_title(f'Изображение 2\n{original2.shape[1]}x{original2.shape[0]}')
    axes[1].axis('off')
    
    axes[2].imshow(result)
    axes[2].set_title(f'Результат\n{result.shape[1]}x{result.shape[0]}')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()

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
        create_test_images()
        
        print("Загрузка изображений...")
        image1 = load_image(args.image1)
        image2 = load_image(args.image2)
        
        print(f"Изображение 1: {image1.shape[1]}x{image1.shape[0]}")
        print(f"Изображение 2: {image2.shape[1]}x{image2.shape[0]}")
        
        print(f"Соединение изображений ({args.direction})...")
        result = stitch_images(image1, image2, args.direction)
        
        print(f"Результат: {result.shape[1]}x{result.shape[0]}")
        
        print("Отображение результатов...")
        display_images(image1, image2, result)
        
        print("Сохранение результата...")
        save_image(result, args.output)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()