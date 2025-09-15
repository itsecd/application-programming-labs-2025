import re
import argparse
from typing import List, Tuple



def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", type=str,required=True, help="Имя входного файла")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Имя выходного файла")
    return parser.parse_args()

def read_file(filename: str) -> str:
    """
    чтение одержимого файла
    """
    with open(filename,'r', encoding="utf-8") as file:
        return file.read()

def extracting_last_name_date_of_birth(data:str) -> List[Tuple[str, str]]:
    """
    выделение из всех данных только
    Фамилии и дат рождения
    """
    pattern = r'Фамилия:\s*([^\n0-9]+)\s*(?:.*?\n)*?Дата рождения:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})'
    return re.findall(pattern, data, re.IGNORECASE)

def normalize_date(date_of_birth: str) -> str:
    """
    приведение даты к единому формату YYYY-MM-DD
    """
    date = date_of_birth.strip() # удаляю пробелы по бокам

    normal_date = re.sub(r'[/.]', '-', date)
    day, month, year = normal_date.split('-')

    day = day.zfill(2)
    month = month.zfill(2)

    return f"{year}-{month}-{day}"

def check_date(date: str) -> bool:
    """
    проверка даты
    """

    part_date = re.split(r'[-]', date) 

    if len(part_date[2]) != 2 or len(part_date[1]) !=2 or len(part_date[0]) != 4:
        return False


    day = int(part_date[2])
    month = int(part_date[1])
    year = int(part_date[0])

    #проверка на адекватность даты
    if not(1<= day <= 31) or not(1 <= month <= 12) or not(1900 <= year < 2026):
        return False
    # проверка на февраль
    if month == 2 and day > 29:
        return False
    # проверка на адекватность даты в месяцах с 30 днями
    if month in [4,6,9,11] and day > 30:
        return False

    return True

def sort_date(data: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    сортировка по дате рождения
    """

    sorted_last_name_and_date_of_birth : List[Tuple[str, str]] = []
    unformat_date: List[Tuple[str, str]] = []

    for last_name, date_of_birth in data:
        norm_date = normalize_date(date_of_birth)
        if check_date(norm_date):
           unformat_date.append((last_name, norm_date))

    unformat_date.sort(key=lambda x: x[1])

    for last_name, date_of_birth in unformat_date:
        norm_format_date = return_format_date(date_of_birth)
        sorted_last_name_and_date_of_birth.append((last_name, norm_format_date))

    return sorted_last_name_and_date_of_birth


def return_format_date(YYYY_format: str) -> str:
    """
    возврат даты в подходящий формат DD-MM-YYYY
    """
    year, month, day = YYYY_format.split('-')
    return f"{day}-{month}-{year}"


def format_in_output(data: List[Tuple[str, str]]) -> List[str]:
    """
    Перевод в конечный формат List
    """

    data_output = []

    for last_name, date_of_birth in data:
        data_output.append(f"{last_name}: {date_of_birth}")
    return data_output

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

    except FileNotFoundError:
        print("ОШИБКА: файл не найден")

    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()






