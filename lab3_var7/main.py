import argparse
import os


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """

    parser = argparse.ArgumentParser(description='Преобразование изображения в бинарное')
    parser.add_argument('-i', '--input', type=str, required=True,
                       help='Путь к исходному изображению')
    parser.add_argument('-o', '--output', type=str, default='binary_result.jpg',
                       help='Путь для сохранения обработанного изображения')
    parser.add_argument('-th', '--threshold', type=int, default=127,
                       help='Порог для бинаризации (0-255)')
    return parser.parse_args()


def main() -> None:

    args = parse_arguments()


if __name__ == "__main__":
    main()