import argparse
import re
from datetime import datetime, date
from typing import List, Tuple


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Имя входного файла")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Имя выходного файла")
    return parser.parse_args()


def read_file(filename: str) -> str:
    """
    чтение одержимого файла
    """
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не был найден")


def extracting_last_name_date_of_birth(data: str) -> List[Tuple[str, str]]:
    """
    выделение из всех данных только
    Фамилии и дат рождения
    """
    pattern = r'Фамилия:\s*([^\n0-9]+)\s*(?:.*?\n)*?Дата рождения:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})'
    return re.findall(pattern, data)


def normalize_date(date_of_birth: str) -> str:
    """
    приведение даты к единому формату DD-MM-YYYY
    """

    date = date_of_birth.strip()  # удаляю пробелы по бокам

    normalized_date = re.sub(r'[/.]', '-', date)
    day, month, year = normalized_date.split('-')

    day = day.zfill(2)
    month = month.zfill(2)

    return f"{day}-{month}-{year}"


def is_date_correct(date: str) -> bool:
    """
    проверка даты
    """
    try:
        part_date = re.split(r'[-]', date)

        day = int(part_date[0])
        month = int(part_date[1])
        year = int(part_date[2])

        year_now = datetime.today().year

        datetime(year, month, day)

        if not (1900 <= year <= year_now):
            return False
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def sort_date(data: List[Tuple[str, str]]) -> List[Tuple[str, date]]:
    """
    сортировка по дате рождения
    """

    sorted_last_name_and_date_of_birth: List[Tuple[str, date]] = []

    for last_name, date_of_birth in data:
        normalized_date = normalize_date(date_of_birth)
        if is_date_correct(normalized_date):
            normalized_date = datetime.strptime(normalized_date, "%d-%m-%Y").date()
            sorted_last_name_and_date_of_birth.append((last_name, normalized_date))

    sorted_last_name_and_date_of_birth.sort(key=lambda x: x[1])

    return sorted_last_name_and_date_of_birth


def format_in_output(data: List[Tuple[str, date]]) -> List[str]:
    """
    Перевод в конечный формат List
    """

    return [f"{last_name}: {date_of_birth}" for last_name, date_of_birth in data]


def write_to_file(filename: str, all_data: List[str]) -> None:
    with open(filename, 'w', encoding="utf-8") as file:
        for data in all_data:
            file.write(data + '\n')


def main() -> None:
    """
    основная функция программы
    """

    try:
        args = parse_arguments()

        all_data = read_file(args.input_file)

        last_name_date = extracting_last_name_date_of_birth(all_data)

        sort_last_name_date = sort_date(last_name_date)

        list_sort_date = format_in_output(sort_last_name_date)

        write_to_file(args.output_file, list_sort_date)
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()
