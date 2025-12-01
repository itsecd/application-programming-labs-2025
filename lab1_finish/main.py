import argparse
from typing import List, Tuple, Optional

from file_utils import read_file, save_to_file
from extractor import extract_phonebook_data


def display_results(data: List[Tuple[str, str]]) -> None:
    if not data:
        print("Не найдено данных для отображения.")
        return

    for surname, phone in data:
        print(f"{surname}: {phone}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Обработка телефонной книги.")
    parser.add_argument("input_file", help="Путь к входному файлу")
    parser.add_argument("-o", "--output", help="Путь к выходному файлу", default=None)

    args = parser.parse_args()

    print(f"Открываем файл: {args.input_file}")

    lines: List[str] = read_file(args.input_file)
    if not lines:
        print("Файл пуст или не удалось прочитать.")
        return

    print(f"Прочитано строк: {len(lines)}")

    phonebook_data = extract_phonebook_data(lines)

    if not phonebook_data:
        print("Не найдено валидных записей.")
        return

    # если указан -o, то сохраняем туда
    output_file: Optional[str] = save_to_file(phonebook_data, args.output)

    display_results(phonebook_data)

    if output_file:
        print(f"\nРезультат сохранён в файл: {output_file}")


if __name__ == "__main__":
    main()
