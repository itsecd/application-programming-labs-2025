from typing import List, Tuple, Optional
from file_utils import read_file, save_to_file
from extractor import extract_phonebook_data


def display_results(data: List[Tuple[str, str]]) -> None:
    """Выводит результаты на экран"""
    if not data:
        print("Не найдено данных для отображения.")
        return
    for surname, phone in data:
        print(f"{surname}: {phone}")


def main() -> None:
    """Основная функция, координирующая работу всех остальных функций"""
    filename: str = r"F:\Python labs\lab1_finish\data.txt"

    print(f"Пытаемся открыть файл: {filename}")

    lines: List[str] = read_file(filename)
    if not lines:
        print("Файл пуст или не удалось прочитать")
        return

    print(f"Прочитано строк: {len(lines)}")

    phonebook_data: List[Tuple[str, str]] = extract_phonebook_data(lines)

    if not phonebook_data:
        print("Не найдено валидных записей с номерами телефонов.")
        return

    output_file: Optional[str] = save_to_file(phonebook_data)

    display_results(phonebook_data)

    if output_file:
        print(f"\nРезультат сохранен в файл: {output_file}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
