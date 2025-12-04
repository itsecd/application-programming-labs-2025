"""
Считать изображение из файла.
Вывести размер изображения.
Сделайте изображение бинарным.
Использовать matplotlib для демонстрации исходного изображения и результата.
Сохранить результат в новый файл.
Путь к исходному файлу, путь для сохранения, параметры по варианту (если есть) необходимо передавать через аргументы командной строки.
"""

import argparse
from pathlib import Path

from im_manag import (
    ImageProcessor
)

def parse_arguments() -> argparse.Namespace:
    """
    Передача аргументов через командную строку
    """

    parser = argparse.ArgumentParser(
        description="Преобразование изображения в бинарный вид"
    )
    parser.add_argument("input_path", type=Path, help="Путь к исходному изображению")
    parser.add_argument("output_path", type=Path, help="Путь для сохранения результата")
    return parser.parse_args()



def main() -> None:
    args = parse_arguments()

    try:
        processor = ImageProcessor(
            input_path=args.input_path, output_path=args.output_path
        )
        processor.load_image()
        width, height = processor.get_image_size()
        print(f"Размер изображения: ширина={width}px, высота={height}px")
        processor.convert_to_binary()
        processor.save_image()
        processor.display_images()

    except Exception as e:
        print(f"Произошла ошибка: {e}")



if __name__ == "__main__":
    main()
