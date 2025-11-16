import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import sys

def add_white_noise(image, noise_intensity=25):
    """
    Накладывает белый шум на изображение
    """
    image_float = image.astype(np.float32)
    noise = np.random.normal(0, noise_intensity, image.shape).astype(np.float32)
    noisy_image = image_float + noise
    noisy_image = np.clip(noisy_image, 0, 255)
    return noisy_image.astype(np.uint8)

def main():
    parser = argparse.ArgumentParser(
        description='Наложение белого шума на изображение',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python main.py input.jpg output.jpg
  python main.py photo.png result.png --noise_intensity 40
        '''
    )
    parser.add_argument('input_path', type=str, help='Путь к исходному изображению')
    parser.add_argument('output_path', type=str, help='Путь для сохранения результата')
    parser.add_argument('--noise_intensity', type=float, default=25.0, 
                       help='Интенсивность шума (стандартное отклонение, по умолчанию: 25)')
    
    args = parser.parse_args()
    
    # Проверка входного файла
    input_path = Path(args.input_path)
    if not input_path.exists():
        print(f"Ошибка: файл {args.input_path} не существует")
        sys.exit(1)
    
    if args.noise_intensity <= 0:
        print("Ошибка: интенсивность шума должна быть положительным числом")
        sys.exit(1)
    
    # Загрузка изображения
    image = cv2.imread(args.input_path)
    if image is None:
        print(f"Ошибка: не удалось загрузить изображение {args.input_path}")
        print("Поддерживаемые форматы: JPEG, PNG, BMP, TIFF и др.")
        sys.exit(1)
    
    # Преобразование BGR в RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Вывод информации о размере
    height, width, channels = image.shape
    print(f"Размер изображения: {width} x {height} пикселей")
    print(f"Количество каналов: {channels}")
    print(f"Интенсивность шума: {args.noise_intensity}")
    
    # Применение белого шума
    noisy_image = add_white_noise(image_rgb, args.noise_intensity)
    
    # Визуализация с помощью matplotlib
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title('Исходное изображение')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(noisy_image)
    plt.title(f'Изображение с белым шумом\n(интенсивность: {args.noise_intensity})')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Сохранение результата
    noisy_image_bgr = cv2.cvtColor(noisy_image, cv2.COLOR_RGB2BGR)
    success = cv2.imwrite(args.output_path, noisy_image_bgr)
    
    if success:
        print(f"Результат успешно сохранен в: {args.output_path}")
    else:
        print(f"Ошибка: не удалось сохранить результат в {args.output_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()