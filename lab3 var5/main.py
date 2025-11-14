from image_processor import process_image, ImageProcessor
import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Парсер аргументов командной строки.

    :return: объект Namespace с аргументами
    """
    parser = argparse.ArgumentParser(description="Инверсия цветов изображения.")
    parser.add_argument("input_file", help="Путь к исходному изображению.")
    parser.add_argument("output_file", help="Путь для сохранения обработанного изображения.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    process_image(args.input_file, args.output_file)