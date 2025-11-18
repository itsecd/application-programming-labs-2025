import argparse
from pathlib import Path
from typing import NoReturn, Optional

from image_processing import process_image_crop
from visualization import display_images_comparison


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description='Обрезка изображения до заданных размеров от левого верхнего угла',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --input photo.jpg --output cropped.jpg --width 500 --height 400
  %(prog)s --input ./images/cat.png --output ./output/cat_crop.png --width 300 --height 300
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Путь к исходному изображению'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Путь для сохранения обрезанного изображения'
    )
    parser.add_argument(
        '--width',
        type=int,
        required=True,
        help='Ширина обрезанного изображения в пикселях'
    )
    parser.add_argument(
        '--height',
        type=int,
        required=True,
        help='Высота обрезанного изображения в пикселях'
    )
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Optional[str]:
    """
    Проверяет корректность аргументов.
    """
    if not Path(args.input).exists():
        return f"Ошибка: файл {args.input} не найден"
    
    if args.width <= 0 or args.height <= 0:
        return "Ошибка: ширина и высота должны быть положительными числами"
    
    return None


def main() -> None:
    args = parse_arguments()
    
    # Валидация аргументов
    error_message = validate_arguments(args)
    if error_message:
        print(error_message)
        return
    
    # Обработка изображения
    try:
        original_img, cropped_img = process_image_crop(
            args.input, 
            args.output, 
            args.width, 
            args.height
        )
        
        # Визуализация результата
        display_images_comparison(
            original_img, 
            cropped_img,
            "Исходное изображение",
            "Обрезанное изображение"
        )
        
        print("\nОбработка завершена успешно!")
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


if __name__ == '__main__':
    main()