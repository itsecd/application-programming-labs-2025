import argparse
import re

def parse_arguments() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file path")
    args = parser.parse_args()
    return args.input

def read_file(name:str) -> str:
    print(f"Чтение файла {name}")
    try:
        with open(name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {name} не найден.")
    except Exception as e:
        raise Exception(f"Ошибка при чтении: {e}")

def write_file(name:str, ovas:list[str]) -> None:
    try:
        with open(name, "w", encoding="utf-8") as file:
            file.write("\n\n".join(ovas))
            print(f"Найденные анкеты сохранены в файл {name}")
    except Exception as e:
        raise Exception(f"Ошибка при записи: {e}")

def find_ovas(data:str) -> list[str]:
    people = re.split(r'\n\n', data)
    ovas = []
    for person in people:
        if re.search(r'Фамилия: \w+ова?\n', person):
            ovas.append(person)
    return ovas

def main() -> None:
    try:
        input_file = parse_arguments()
        data = read_file(input_file)
        ovas = find_ovas(data)
        print(f"Найдено {len(ovas)} анкет людей, чьи фамилии заканчиваются на 'ов(а)'")
        if ovas:
            write_file("ovas_profiles.txt", ovas)
    except Exception as e:
        print(f"Возникла ошибка: {e}")

if __name__ == "__main__":
    main()
