import argparse
import re


def parse_command_line_arguments() -> str:
    """
    Разбирает аргументы командной строки
    Returns: имя файла с анкетами
    """
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("input_file", type=str, help = "File_name")
    args = parser.parse_args()
    return args.input_file


def read_file(filename: str) -> list:
    """
    Построчное чтение файла
    :param filename: имя файла
    :return: список строк файла
    """

    with open(filename, "r") as file:
        lines = file.readlines()
        return lines

def main() -> None:
    # Получение имени файла с анкетами из командной строки
    file_name = parse_command_line_arguments()

    # Чтение файла по строчно
    lines = read_file(file_name)
    print(lines)

if __name__ == "__main__":
    main()
