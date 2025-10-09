import argparse
import re


def parser_file() -> argparse.Namespace:
    """Функция для парсинга аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Путь к файлу")
    parser.add_argument("name", type=str, help="Имя для поиска")
    return parser.parse_args()


def read_file(filepath: str) -> str | None:
    """
    Функция для чтения из файла
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as ex:
        raise FileNotFoundError(f"файл '{filepath}' не найден: {ex}")


def clean_records(filepath: str) -> list[str]:
    """
    Разбивает текст на анкеты по двойному переносу строки
    """
    text = read_file(filepath)
    blocks = text.split("\n\n")
    records = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            records.append(cleaned_block)
    return records


def get_full_records_by_name(name: str, records: list[str]) -> list[str]:
    """
    Функция для проверки анкет по имени
    Сначала передаем имя которое ввел пользователь 'name'
    далее создаем список в котором будут храниться нужные анкеты
    проводим проверку с анкетами и функция возвращает список анкет
    """

    found_records = []
    for record in records:
        lines = record.splitlines()
        for line in lines:
            match = re.match(r"^Имя:\s*(.+)", line)
            if match:
                record_name = match.group(1).strip()
                if record_name.lower() == name.lower():
                    found_records.append(record)
                break

    return found_records


def write_file(found_records: list[str]) -> None:
    """
    функция для записи в файл

    """
    try:
        with open("data1.txt", "w", encoding="utf-8") as file:
            for record in found_records:
                file.write(record + "\n\n")
    except PermissionError:
        raise ("Недостаточно прав для выполнения оперции")


def main() -> None:
    args = parser_file()
    name = args.name.lower()

    try:
        records = clean_records(args.file)
        found_records = get_full_records_by_name(name, records)
        write_file(found_records)
        total = len(found_records)
        print(f"Людей с именем '{name}' найдено {total} человек")
    except Exception as ex:
        print(f"Произошла ошибка: {ex}")


if __name__ == "__main__":
    main()
