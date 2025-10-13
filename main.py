import re
from datetime import datetime


def is_valid_name(name: str) -> bool:
    if not name or not name[0].isupper():
        return False
    return (
        r"[А-ЯЁа-яёA-Za-z]+", name) is not None


def normalize_gender(gender: str) -> str:
    g = gender.strip()
    if g in {"М", "м", "Мужской", "мужской"}:
        return "М"
    if g in {"Ж", "ж", "Женский", "женский"}:
        return "Ж"
    return "-"


def is_valid_gender(gender: str) -> bool:
    return normalize_gender(gender) != "-"


def normalize_date(date_str: str) -> str:
    formats = [
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%y",
        "%d-%m-%y",
        "%d/%m/%y",
        "%d %m %Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if 1900 <= dt.year <= 2024:
                # Проверка корректности самой даты (например, 31.02 —
                # недопустимо)
                try:
                    datetime.strptime(dt.strftime("%d.%m.%Y"), "%d.%m.%Y")
                    return dt.strftime("%d.%m.%Y")
                except ValueError:
                    continue
        except ValueError:
            continue
    return "-"


def is_valid_date(date_str: str) -> bool:
    """Проверяет корректность даты рождения."""
    return normalize_date(date_str) != "-"


def normalize_contact(contact: str) -> str:
    contact = contact.strip()
    digits = re.sub(r"\D", "", contact)
    if len(digits) == 11 and digits[0] in "78":
        return f"8 ({digits[1:4]}) {digits[4:7]} {digits[7:9]} {digits[9:]}"
    if re.fullmatch(
        r"[a-zA-Z0-9._%+-]+@(gmail\.com|mail\.ru|yandex\.ru)",
        contact
    ):
        return contact
    return "-"


def is_valid_contact(contact: str) -> bool:
    return normalize_contact(contact) != "-"


def normalize_city(city: str) -> str:
    city = city.strip()
    if city.startswith("г."):
        city = city[2:].strip()
    if len(city) > 64 or not city or not any(c.isalpha() for c in city):
        return "-"
    return city


def main() -> None:
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()

    entries = re.split(r"\n\d+\)\s*", content)[1:]
    results = []

    for entry in entries:
        lines = [
            line.strip()
            for line in entry.strip().split("\n")
            if line.strip()
        ]
        data = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        surname = data.get("Фамилия", "")
        name = data.get("Имя", "")
        gender = data.get("Пол", "")
        birth = data.get("Дата рождения", "")
        contact = data.get("Номер телефона или email", "")
        city = data.get("Город", "")

        norm_surname = surname if is_valid_name(surname) else "-"
        norm_name = name if is_valid_name(name) else "-"
        norm_gender = (
            normalize_gender(gender) if is_valid_gender(gender) else "-"
        )
        norm_date = normalize_date(birth) if is_valid_date(birth) else "-"
        norm_contact = (
            normalize_contact(contact) if is_valid_contact(contact) else "-"
        )
        norm_city = normalize_city(city)

        line = (
            f"{norm_surname} {norm_name} {norm_gender} "
            f"{norm_date} {norm_contact} "
            f"{norm_city}"
        )
        results.append(line)

    with open("result.txt", "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")

    print("Обработка завершена. Результат в файле 'result.txt'")


if __name__ == "__main__":
    main()
