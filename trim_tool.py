import argparse
from pathlib import Path
from typing import Optional

from image_utils import execute_image_trimming
from image_viewer import show_image_comparison


def get_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    
    argument_parser = argparse.ArgumentParser(
        description='Обрезка изображения до заданных размеров от левого верхнего угла'
    )

    argument_parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='Путь к исходному изображению'
    )
    argument_parser.add_argument(
        '--result',
        type=str,
        required=True,
        help='Путь для сохранения обрезанного изображения'
    )
    argument_parser.add_argument(
        '--width',
        type=int,
        required=True,
        help='Ширина обрезанного изображения в пикселях'
    )
    argument_parser.add_argument(
        '--height',
        type=int,
        required=True,
        help='Высота обрезанного изображения в пикселях'
    )

    return argument_parser.parse_args()


def check_arguments(params: argparse.Namespace) -> Optional[str]:
    """
    Проверяет корректность аргументов.
    """

    if not Path(params.source).exists():
        return f"Ошибка: файл {params.source} не найден"

    if params.width <= 0 or params.height <= 0:
        return "Ошибка: ширина и высота должны быть положительными числами"

    return None


def run() -> None:
    params = get_arguments()

    validation_error = check_arguments(params)
    if validation_error:
        print(validation_error)
        return

    try:
        source_image, trimmed_image = execute_image_trimming(
            params.source, 
            params.result, 
            params.width, 
            params.height
        )

        show_image_comparison(
            source_image, 
            trimmed_image,
            "Исходное изображение",
            "Обрезанное изображение"
        )

        print("\nОбработка завершена успешно!")

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")


if __name__ == '__main__':
    run()