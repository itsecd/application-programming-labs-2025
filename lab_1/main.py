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


def args_parse() -> tuple[str, str]:
    """
    Эта функция парсит аргументы из консоли
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    if args.output is not None:
        return (args.input, args.output)
    else:
        raise Exception("The name of ouput file can'b be None")


def main() -> None:
    pass

if __name__ == "__main__":
    main()