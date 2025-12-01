import argparse
import matplotlib.pyplot as plt
from functions import create_pixel_art, read_image, convert_bgr_to_rgb, convert_rgb_to_bgr, save_image, display_images

def main():
    """Основная функция для преобразования изображения в пиксель-арт."""
    
    try:
        # Парсинг аргументов командной строки
        parser = argparse.ArgumentParser(description='Преобразование изображения в пиксель-арт')
        parser.add_argument('--input_path', default='00001.jpg', help='Путь к исходному изображению')
        parser.add_argument('--output_path', default='pixel_art_result.jpg', help='Путь для сохранения результата')
        parser.add_argument('--pixel_size', type=int, default=10, help='Размер пикселя')
        
        args = parser.parse_args()
        
        # Чтение изображения
        img = read_image(args.input_path)
        
        # Конвертация из BGR в RGB
        img_rgb = convert_bgr_to_rgb(img)
        
        # Вывод размера изображения
        print(f"Размер изображения: {img.shape[1]} x {img.shape[0]} пикселей")
        print(f"Количество каналов: {img.shape[2]}")
        
        # Преобразование в пиксель-арт
        pixel_art = create_pixel_art(img_rgb, args.pixel_size)
        
        # Отображение исходного изображения и результата
        display_images(img_rgb, pixel_art, args.pixel_size)
        
        # Сохранение результата
        pixel_art_bgr = convert_rgb_to_bgr(pixel_art)
        save_image(pixel_art_bgr, args.output_path)
        print(f"Результат сохранен в: {args.output_path}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
