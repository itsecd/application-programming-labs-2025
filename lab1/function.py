import argparse
import io
import re


def read_file(filename: str) -> str:
    """
    Reading file for his path
    """
    try:
        file = open(filename, "r")
        print(f"File {filename} is parsed!")
        text = file.read()
        file.close()
        return text
    except FileNotFoundError:
        print(f"Sorry, {filename} dont found!!!")
        return ""


def is_correct(date: str) -> bool:
    """
    check date for correctness
    """
    if not re.fullmatch(
            r'(0?[1-9]|[12][0-9]|[3][01])[./-]+(0?[1-9]|[1][012])[./-]+'
            r'([1][9][0-9]{2}|[2][0][01][0-9]|[2][0][2][0-5])', date):
            return False
    else:
            return True


def to_file(file: io.TextIOWrapper, men: str) -> None:
    """
    data of one people output to file
    """
    file.write(men)
    file.write("\n")


def get_args() -> str:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()  # создание экземпляра парсера
    parser.add_argument('filename', type=str, help='filename')  # добавление позиционного аргумента командной строки
    args = parser.parse_args()  # парсинг аргументов
    if args.filename is None:
        return ""
    return args.filename
