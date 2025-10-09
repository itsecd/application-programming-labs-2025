import argparse
import re


def read_file(filenamedata: str) -> str:
    """
    открытие файла
    """
    try:
        with open(filenamedata, "r", encoding="utf-8") as file:
            text_file = file.read()
            return text_file
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")


def search_moscow_ankets(text_file: str) -> list[str]:
    """
    поиск нужных анкет
    """
    ankets = re.findall(r"\d+\)\n(?:.*\n)+?(?=\d+\)|$)", text_file)
    moscow = []
    for anketa in ankets:
        if re.search(r"Город:\s*[г.\s*]Москва", anketa):
            moscow.append(anketa)
    return moscow


def write_data(filenameoutput: str, Moscow_list: list) -> None:
    """
    запись в другой файл
    """
    with open(filenameoutput, "w", encoding="utf-8") as file_1:
        for anketa in Moscow_list:
            file_1.write(anketa)


def parsing() -> tuple[str, str]:
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenamedata", type=str, help="Введите путь файла")
    parser.add_argument(
        "filenameoutput", type=str, help="Введите путь файла для вывода"
    )
    args = parser.parse_args()
    return args.filenamedata, args.filenameoutput


def main() -> None:
    try:
        filename_data, filename_output = parsing()
        text_file = read_file(filename_data)
        moscow_ankets = search_moscow_ankets(text_file)
        print(len(moscow_ankets))
        write_data(filename_output, moscow_ankets)

    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()
