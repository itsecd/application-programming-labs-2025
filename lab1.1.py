import argparse
import re


def parser_file():
    """Функция для парсинга аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Путь к файлу")
    parser.add_argument("name", type=str, help="Имя для поиска")
    return parser.parse_args()


def read_file(filepath: str) -> str:
    """
    Функция для чтения из файла
    Возвращает содержимое файла как строку
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    except FileNotFoundError as exs:
        print(f"Error: {exs}")
        return None


def get_full_records_by_name(name: str, filepath: str) -> list[str]:
    """
    Функция для проверки анкет по имени
    Сначала передаем имя которое ввел пользователь 'name'
    далее создаем список в котором будут храниться нужные анкеты
    проводим проверку с анкетами и функция возвращает список анкет
    """
    text = read_file(filepath)
    if text is None:
        return []

    blocks = text.split("\n\n")
    records = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            records.append(cleaned_block)

    found_records = []
    for record in records:
        lines = record.splitlines()
        for line in lines:
            if line.startswith("Имя:"):
                parts = line.split(":", 1)
                record_name = parts[1]
                record_name = record_name.strip()
                record_name = record_name.lower()
                if re.search(name, record_name):
                    found_records.append(record)
                    break
    return found_records


def write_file(found_records: list[str]) -> None:
    """
    функция для записи в файл
    """
    try:
        with open("data1.txt", "w", encoding="utf-8") as file:
            for exit_file in found_records:
                file.write(exit_file + "\n\n")
    except Exception as exs:
        print(f"Error при записи: {exs}")


def main() -> None:
    """
    главная функция которая управляет кодом
    """
    args = parser_file()
    name = args.name.lower()
    found_records = get_full_records_by_name(name, args.file)
    write_file(found_records)
    total = len(found_records)
    print("Людей с именем ", name, "найдено ", total, "человек")


if __name__ == "__main__":
    main()
