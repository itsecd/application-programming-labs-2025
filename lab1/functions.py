import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def read_file(file_path: str) -> str:
    # Читает содержимое файла.
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {file_path}") from e
    except IOError as e:
        raise IOError(f"Ошибка при ччтении файла {file_path}: {e}") from e


def parse_profiles(text: str) -> List[Dict[str, str]]:
    # Парсит текст и извлекает данные анкет.
    pattern = (
        r"(?:^\s*(\d+)\)\s*[\r\n]+)?"
        r"Фамилия:\s*(.+?)\s*[\r\n]+"
        r"Имя:\s*(.+?)\s*[\r\n]+"
        r"Пол:\s*(.+?)\s*[\r\n]+"
        r"Дата рождения:\s*(.+?)\s*[\r\n]+"
        r"Номер телефона или email:\s*(.+?)\s*[\r\n]+"
        r"Город:\s*(.+?)(?=(?:[\r\n]+(?:\d+\)|Фамилия:)|\Z))"
    )

    matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
    profiles: List[Dict[str, str]] = []

    for match in matches:
        num_str = match[0].strip() if match[0] else ""
        number: Optional[int] = int(num_str) if num_str else None

        profile = {
            "number": number,
            "surname": match[1].strip(),
            "name": match[2].strip(),
            "gender": match[3].strip(),
            "birthdate": match[4].strip(),
            "contact": match[5].strip(),
            "city": match[6].strip(),
        }
        profiles.append(profile)

    return profiles


def is_valid_date(date_str: str) -> bool:
    # Проверка корректности даты рождения.
    pattern = r"^(\d{1,2})[./-](\d{1,2})[./-](\d{4})$"
    m = re.match(pattern, date_str.strip())
    if not m:
        return False

    day, month, year = map(int, m.groups())
    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        return False

    try:
        datetime(year=year, month=month, day=day)
        return True
    except ValueError:
        return False


def parse_date(date_str: str) -> datetime:
    # Преобразует строку с датой в объект datetime.
    if not is_valid_date(date_str):
        raise ValueError(f"Формат даты неверный {date_str}")

    normalized = re.sub(r"[./]", "-", date_str.strip())
    day, month, year = map(int, normalized.split("-"))
    return datetime(year=year, month=month, day=day)


def calculate_age(birthdate: datetime) -> int:
    # Считает возраст (его вывод будет в конце анкеты).
    today = datetime.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age


def find_oldest_and_youngest(profiles: List[Dict[str, str]]) -> Tuple[Dict, Dict]:
    # Ищет самого старого и самого молодого человека.
    if not profiles:
        raise ValueError("Пустой список анкет")

    valid_profiles = []
    for profile in profiles:
        try:
            bd = parse_date(profile["birthdate"])
            age = calculate_age(bd)
            profile_with_age = {**profile, "age": age, "birthdate_obj": bd}
            valid_profiles.append(profile_with_age)
        except ValueError:
            continue

    if not valid_profiles:
        raise ValueError("Анкет с валидной датой рождения нет :( ")

    oldest = min(valid_profiles, key=lambda p: p["birthdate_obj"])
    youngest = max(valid_profiles, key=lambda p: p["birthdate_obj"])
    return oldest, youngest


def format_profile(profile: Dict) -> str:
    # Форматирование.
    number = profile.get("number")
    header = f"Номер анкеты: {number}\n" if number is not None else ""
    return (
        header
        + f"Фамилия: {profile['surname']}\n"
        + f"Имя: {profile['name']}\n"
        + f"Пол: {profile['gender']}\n"
        + f"Дата рождения: {profile['birthdate']}\n"
        + f"Контакт: {profile['contact']}\n"
        + f"Город: {profile['city']}\n"
        + f"Возраст: {profile['age']} лет"
    )
