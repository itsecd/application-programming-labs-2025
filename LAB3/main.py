import argparse
import sys
from pathlib import Path

from image_processor import add_white_noise, load_image, save_image
from visualizer import visualize_comparison


def main() -> None:
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
    image = load_image(args.input_path)
    if image is None:
        print(f"Ошибка: не удалось загрузить изображение {args.input_path}")
        print("Поддерживаемые форматы: JPEG, PNG, BMP, TIFF и др.")
        sys.exit(1)
    
    # Преобразование BGR в RGB
    image_rgb = image
    
    # Вывод информации о размере
    height, width, channels = image_rgb.shape
    print(f"Размер изображения: {width} x {height} пикселей")
    print(f"Количество каналов: {channels}")
    print(f"Интенсивность шума: {args.noise_intensity}")
    
    # Применение белого шума
    noisy_image = add_white_noise(image_rgb, args.noise_intensity)
    
    # Визуализация
    visualize_comparison(image_rgb, noisy_image, args.noise_intensity)
    
    # Сохранение результата
    if save_image(noisy_image, args.output_path):
        print(f"Результат успешно сохранен в: {args.output_path}")
    else:
        print(f"Ошибка: не удалось сохранить результат в {args.output_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()