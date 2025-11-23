import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_pixel_art(image, pixel_size=10):
    
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

def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Преобразование изображения в пиксель-арт')
    parser.add_argument('--input_path', default='000001.jpg', help='Путь к исходному изображению (по умолчанию: 000001.jpg)')
    parser.add_argument('--output_path', default='pixel_art_result.jpg', help='Путь для сохранения результата')
    parser.add_argument('--pixel_size', type=int, default=10, help='Размер пикселя (по умолчанию: 10)')
    
    args = parser.parse_args()
    
    # Чтение изображения
    img = cv2.imread(args.input_path)
    
    if img is None:
        print(f"Ошибка: не удалось загрузить изображение {args.input_path}")
        print("Убедитесь, что файл находится в той же папке, что и скрипт")
        return
    
    # Конвертация из BGR в RGB для правильного отображения в matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Вывод размера изображения
    print(f"Размер изображения: {img.shape[1]} x {img.shape[0]} пикселей")
    print(f"Количество каналов: {img.shape[2]}")
    
    # Преобразование в пиксель-арт
    pixel_art = create_pixel_art(img_rgb, args.pixel_size)
    
    # Отображение исходного изображения и результата
    plt.figure(figsize=(12, 6))
    
    # Исходное изображение
    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title('Исходное изображение')
    plt.axis('off')
    
    # Пиксель-арт
    plt.subplot(1, 2, 2)
    plt.imshow(pixel_art)
    plt.title(f'Пиксель-арт (размер пикселя: {args.pixel_size})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Сохранение результата (конвертируем обратно в BGR для OpenCV)
    pixel_art_bgr = cv2.cvtColor(pixel_art, cv2.COLOR_RGB2BGR)
    cv2.imwrite(args.output_path, pixel_art_bgr)
    print(f"Результат сохранен в: {args.output_path}")

if __name__ == "__main__":
    main()

    #py lab3.py --input_path 000001.jpg --output_path result.jpg --pixel_size 15