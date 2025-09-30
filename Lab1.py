import argparse
import re


def parse_arguments() -> str:
    """
    Парсинг аргумента из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file path")
    args = parser.parse_args()
    return args.input


def read_file(input_file:str) -> str:
    """
    Чтение файла input_file
    """
    print(f"Чтение файла {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {input_file} не найден.")
    except Exception as exc:
        raise Exception(f"Ошибка при чтении: {exc}")


def write_file(output_file:str, ovas:list[str]) -> None:
    """
    Запись анкет из ovas в файл output_file
    """
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n\n".join(ovas))
            print(f"Найденные анкеты сохранены в файл {output_file}")
    except Exception as exc:
        raise Exception(f"Ошибка при записи: {exc}")


def find_ovas(data:str) -> list[str]:
    """
    Поиск анкет с фамилиями, заканчивающимися на ов(а)
    """
    profiles = re.split(r'\n\n', data)
    ovas = []
    for profile in profiles:
        if re.search(r'Фамилия: \w+ова?\n', profile):
            ovas.append(profile)
    return ovas


def main() -> None:
    try:
        input_file = parse_arguments()
        data = read_file(input_file)
        ovas = find_ovas(data)
        print(f"Найдено {len(ovas)} анкет людей, чьи фамилии заканчиваются на 'ов(а)'")
        if ovas:
            write_file("ovas_profiles.txt", ovas)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()

