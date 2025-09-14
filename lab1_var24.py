import re
import argparse
from typing import List, Tuple
from time import  localtime

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
    pattern = r'Фамилия:\s*([^\n]+)\s*(?:.*?\n)*?Дата рождения:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})'
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

    penis = re.split(r'[-]', date) # ПОМЕНЯЙ ЕБЛАН

    if len(penis[2]) != 2 or len(penis[1]) !=2 or len(penis[0]) != 4:
        return False


    day = int(penis[2])
    month = int(penis[1])
    year = int(penis[0])

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
    for last_name, date_of_birth in data:
        norm_date = normalize_date(date_of_birth)
        if check_date(norm_date):
           sorted_last_name_and_date_of_birth.append((last_name, norm_date))

    sorted_last_name_and_date_of_birth.sort(key=lambda x: x[1])




    return sorted_last_name_and_date_of_birth

a = read_file("data.txt")
b = extracting_last_name_date_of_birth(a)
c = sort_date(b)
print(c)











