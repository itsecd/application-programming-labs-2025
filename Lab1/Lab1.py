import argparse
import re
from datetime import datetime

def read_file(file_name: str) -> str:
    """открыетие файла"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text_file = file.read()
            return text_file
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")

def parsing() -> str:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, help="type filename")
    args = parser.parse_args()
    return args.file_name

def valid_date(card: str) -> bool:
    """проверка даты на валидность"""
    date = re.search(r'(\d{1,2})([-/.])(\d{1,2})\2(\d{4})', card)
    if not date:
        return False
    day = date.group(1)
    month = date.group(3)
    year = date.group(4)
    try:
        date = datetime.strptime(f"{day}.{month}.{year}", '%d.%m.%Y')
        if date.year >= 1900:
            return True
        return False
    except ValueError:
        return False

def get_cards(data: str) -> dict[int,str]:
    """запись анкет в словарь(для упрощения доступа к отдельным анкетам)"""
    cards_dict = {}
    cards = re.split(r'\d+\)\n', data)
    for i in range(1, len(cards)):
        date = valid_date(cards[i])
        if date:
            cards_dict[i] = cards[i]
    return cards_dict

def get_age(cards: dict, index: int) -> datetime:
    """парсинг и возврат даты в формате datetime"""
    date = re.search(r'(\d{1,2})([-/.])(\d{1,2})\2(\d{4})', cards[index])
    day = date.group(1)
    month = date.group(3)
    year = date.group(4)
    return datetime.strptime(f"{day}.{month}.{year}", '%d.%m.%Y')

def oldest_and_youngest(cards: dict) -> None:
    """поиск самого младшего и самого старшего человека, вывод их анкет"""
    oldest_age = None
    youngest_age = None
    oldest_id = None
    youngest_id = None
    for i in cards:
        age = get_age(cards, i)
        if i == 1:
            oldest_age = age
            youngest_age = age
            oldest_id = i
            youngest_id = i
        if oldest_age > age:
            oldest_age = age
            oldest_id = i
        if youngest_age < age:
            youngest_age = age
            youngest_id = i
    oldest = datetime.now().year - oldest_age.year
    if (datetime.now().month, datetime.now().day) < (oldest_age.month, oldest_age.day):
        oldest -= 1
    youngest = datetime.now().year - youngest_age.year
    if (datetime.now().month, datetime.now().day) < (youngest_age.month, youngest_age.day):
        youngest -= 1
    print(f"Самый старый человек: \nВозраст: {oldest} \nАнкета: \n{cards[oldest_id]}")
    print(f"Самый молодой человек: \nВозраст: {youngest} \nАнкета: \n{cards[youngest_id]}")
    return

def main():
    file_name = parsing()
    data = read_file(file_name)
    cards = get_cards(data)
    oldest_and_youngest(cards)
if __name__ == "__main__":

    main()
