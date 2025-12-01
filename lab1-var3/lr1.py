import argparse
import re
from datetime import datetime
from typing import List, Optional

DATE_PATTERN = re.compile(r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})")


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Извлекает дату из строки и возвращает объект datetime.
    Поддерживаются форматы: DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY.
    Возвращает None, если дата невалидна или не найдена.
    """
    match = DATE_PATTERN.search(date_str)
    if not match:
        return None
    day, month, year = map(int, match.groups())
    if not (1900 <= year <= datetime.now().year):
        return None
    try:
        return datetime(year, month, day)
    except ValueError:
        return None


def age_from_birthdate(birthdate: datetime) -> int:
    """
    Считает возраст в годах на текущую дату.
    """
    today = datetime.now()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age


def read_people_from_file(filename: str) -> List[List[str]]:
    """
    Читает людей из файла.
    Возвращает только тех людей, чей возраст в диапазоне 30–40.
    """
    people: List[List[str]] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла: {e}")

    current_person: List[str] = []
    for line in lines:
        current_person.append(line)
        if line.startswith("Город:") and current_person:
            birth_line = next((l for l in current_person if l.startswith("Дата рождения:")), None)
            if birth_line:
                birth_str = birth_line.split(":", 1)[1].strip()
                bdate = parse_date(birth_str)
                if bdate and 30 <= age_from_birthdate(bdate) <= 40:
                    people.append(current_person)
            current_person = []

    return people


def save_people_to_file(people: List[List[str]], filename: str) -> None:
    """
    Сохраняет список людей в текстовый файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as out:
            for person in people:
                out.write("\n".join(person) + "\n")
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи в файл '{filename}': {e}")


def main():
    """
    Точка входа: парсит аргументы, обрабатывает исключения,
    выводит количество найденных людей и сохраняет результат.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="input file")
    args = parser.parse_args()

    try:
        people_30_40 = read_people_from_file(args.filename)
        print(len(people_30_40))
        save_people_to_file(people_30_40, "result.txt")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()