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
    выделяю из всех данных только
    Фамилию и дату рождения
    """
    pattern = r'Фамилия:\s*([^\n]+)\s*(?:.*?\n)*?Дата рождения:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})'
    return re.findall(pattern, data, re.IGNORECASE)

def normolize_date(date_of_birth: str) -> str:
    """
    привожу даты к единому формату DD.MM.YYYY
    """
    date = date_of_birth.strip() # удаляю пробелы по бокам

    normal_date = re.sub(r'[-/]', '.', date)

    return normal_date

def check_date(date_of_birth: str) -> bool:
    """
    проверка даты
    """
    date = normolize_date(date_of_birth)

    penis = re.split(r'[.]', date) # ПОМЕНЯЙ ЕБЛАН

    day = int(penis[0])
    month = int(penis[1])
    year = int(penis[2])

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

def defining_the_age(date_of_birth: str) -> int:
    date = normolize_date(date_of_birth)
    now_year = localtime(date).tm_year
    penis = re.split(r'[.]', date)  # ПОМЕНЯЙ ЕБЛАН
    year = int(penis[2])
    return now_year - year






