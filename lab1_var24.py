import re
import argparse
from typing import List, Tuple

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









