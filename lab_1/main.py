import re
import argparse


def read_file(path: str) -> str:
    """
    Эта функция возвращает текст как одну большую строку
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except:
        raise Exception("Ошибка при открытии файла")


def main() -> None:
    pass
    

if __name__ == "__main__":
    main()