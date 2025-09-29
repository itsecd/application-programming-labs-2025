import argparse
import re
import io

def readfile(filename: str) -> str:
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
            r'(0?[0-9]|[12][0-9]|[3][01])[./-]+(0?[0-9]|[1][012])[./-]+'
            r'([1][9][0-9]{2}|[2][0][01][0-9]|[2][0][2][0-5])', date):
            return False
    else:
            return True

def print_men(mens: list[str], index:int) -> None:
    """
    data of one people output to cmd
    """
    for i in range(index,index+8):
            print(mens[i])

def to_file(file: io.TextIOWrapper, index: int, mens: list[str]) -> None:
    """
    data of one people output to file
    """
    for i in range(index, index + 8):
            file.write(mens[i])
            file.write("\n")
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
