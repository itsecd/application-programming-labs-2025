import argparse
import sys
import os
from typing import List

try:
    from image_processor import ImageProcessor, BGColor
except ImportError:
    print(
        "Ошибка: Не найден модуль 'image_processor.py'.\n"
        "Убедитесь, что 'main.py' и 'image_processor.py' находятся в одной папке.",
        file=sys.stderr
    )
    sys.exit(1)
except Exception as e:
    print(f"Неожиданная ошибка при импорте image_processor: {e}", file=sys.stderr)
    sys.exit(1)

VALID_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']


def parse_arguments(args: List[str]) -> argparse.Namespace:
    """
    Парсит аргументы командной строки, переданные скрипту.

    Args:
        args (List[str]): Список строковых аргументов, обычно `sys.argv[1:]`.

    Returns:
        argparse.Namespace: Объект, содержащий спарсенные аргументы.
    """
    parser = argparse.ArgumentParser(
        description="Считывает изображение, делает его круглым, "
                    "отображает оригинал и результат, сохраняет результат.",
        epilog="Пример использования: python main.py input.jpg output.png --bg white"
    )
    parser.add_argument(
        "input_file",
        help="Путь к исходному файлу изображения."
    )
    parser.add_argument(
        "output_file",
        help="Путь для сохранения обработанного файла изображения."
    )
    parser.add_argument(
        "--bg_color",
        dest="bg_color",
        help="Цвет фона для области вне круга ('black', 'white' или 'transparent').",
        choices=['black', 'white', 'transparent'],
        default='transparent'
    )

    if not args:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args(args)


def main_workflow(parsed_args: argparse.Namespace) -> None:
    """
    Основной рабочий процесс программы: загрузка, обработка, отображение и сохранение.

    Args:
        parsed_args (argparse.Namespace): Объект с аргументами командной строки.
    """
    input_path: str = parsed_args.input_file
    output_path: str = parsed_args.output_file
    bg_color: BGColor = parsed_args.bg_color

    if not os.path.exists(input_path):
        print(f"Ошибка: Входной файл не найден по пути: '{input_path}'", file=sys.stderr)
        sys.exit(1)

    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    if ext not in VALID_IMAGE_EXTENSIONS:
        print(f"Ошибка: Неподдерживаемый формат изображения '{ext}'.", file=sys.stderr)
        print(f"Поддерживаемые форматы: {', '.join(VALID_IMAGE_EXTENSIONS)}", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Загрузка изображения: '{input_path}'...")
        processor = ImageProcessor(input_path)
        print(processor.get_image_size_info())

        print(f"Создание круглого изображения с фоном '{bg_color}'...")
        circular_image = processor.make_circular(bg_color)

        print(f"Сохранение результата в: '{output_path}'...")
        processor.save_result_image(output_path, circular_image)
        print("Изображение успешно сохранено.")

        print("Отображение сравнения оригинала и результата...")
        processor.display_comparison(circular_image)

    except IOError as e:
        print(f"Ошибка ввода/вывода при обработке изображения: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    main_workflow(args)