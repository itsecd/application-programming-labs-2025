"""
Основной модуль программы.
Обрабатывает аргументы командной строки и координирует обработку файла.
"""

import argparse

from file_utils import read_file, write_file, extract_and_format_names


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", type=str, help="Имя входного файла")
    parser.add_argument("output_filename", type=str, help="Имя выходного файла")
    return parser.parse_args()


def main() -> None:
    """
    Основная функция программы.

    """
    args = parse_arguments()
    output_filename = "data_new.txt"

    try:
        content = read_file(args.input_filename)
        formatted_names = extract_and_format_names(content)
        formatted_names.sort()
        write_file(args.output_filename, formatted_names)
        print("Новый файл сохранен")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()