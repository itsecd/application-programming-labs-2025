import argparse
import calendar
import re

# Кокшина Анна Александровна 6211-100503

def correct_data(data: str) -> bool:
    """ Функция проверяет корректоность написания даты"""
    if not re.fullmatch(r"\d{1,2}[./-]\d{1,2}[./-]\d{4}", data):
        return False
    day, month, year = map(int, re.split(r"[/.-]+", data))
    if not 1 <= month <= 12:
        return False
    elif not (1 <= day <= calendar.monthrange(year, month)[1] and 1900 <= year <= 2025):
        return False
    return True

def correct_phone(phone: str) -> bool:
    """Функция проверяет корректность номера телефона"""
    return re.fullmatch(r"(?:8|\+7)\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}", phone)

def correct_email(email: str) -> bool:
    """Функция проверяет корректность указанной почты"""
    if not re.fullmatch(r"[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)", email):
        return False
    return True

def correct_person(person: list) -> bool:
    """ Функция проверяет анкету человека"""
    if person[0][0].islower() or person[1][0].islower():
        return False
    if person[2] not in [
        "М",
        "м",
        "Мужской",
        "мужской",
        "Ж",
        "ж",
        "Женский",
        "женский",
    ]:
        return False
    if not correct_data(person[3]):
        return False
    if not (correct_phone(person[4]) or correct_email(person[4])):
        return False
    return True

def read_file(file_name: str) -> str:
    """ Считывает файл и возвращает строки, если файд не открыт - None"""
    try:
        with open(file_name, "r", encoding="utf8") as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError

def print_result(names: dict[str, int]) -> None:
    """ Функция находит часто встрещающееся имя и выводит его"""
    max_count = 0
    max_name = ""
    for name, count in names.items():
        if max_count < count:
            max_count = count
            max_name = name
    print(f"Самое частое имя {max_name} и количество повторений: {max_count}")

def main() -> None:
    parser = argparse.ArgumentParser()  # создание экземпляра парсера
    parser.add_argument('file_name', type=str, help='Укажите путь к файлу')  # добавление позиционного аргумента командной строки
    args = parser.parse_args()  # парсинг аргументов
    try:
        data = read_file((args.file_name))
    except:
        print("Ошибка открытия файла")
        exit(1)
    person = []
    names = {}
    for line in data:
        if re.fullmatch(r"\d+[)]\n", line) or line == "\n":
            person.clear()
            continue
        person.append(line[line.find(":")+2:-1])
        if len(person) == 6:
            if not correct_person(person):
                continue
            if person[1] not in names:
                names[person[1]] = 1
            else:
                names[person[1]] += 1
    print_result(names)

if __name__ == "__main__":
    main()

