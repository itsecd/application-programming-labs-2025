import re
from typing import List, Tuple

SEARCH_RANGE = 10   # сколько строк после фамилии искать телефон


def format_phone_number(phone_line: str, clean_pattern: str) -> str:
    """Форматирует номер в вид +7(XXX)XXX-XX-XX"""
    clean = re.sub(clean_pattern, "", phone_line)

    if len(clean) != 11:
        return phone_line  # оставить как есть

    # нормализация: 8XXXXXXXXXX -> 7XXXXXXXXXX
    if clean.startswith("8"):
        clean = "7" + clean[1:]

    return f"+7({clean[1:4]}){clean[4:7]}-{clean[7:9]}-{clean[9:]}"


def extract_phonebook_data(lines: List[str]) -> List[Tuple[str, str]]:
    """Извлекает (Фамилия, Телефон) из списка строк."""
    
    surname_pattern = r'^Фамилия:\s*([А-ЯЁ][а-яё]*)$'
    phone_pattern = r'^(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    clean_pattern = r'[^\d]'

    result: List[Tuple[str, str]] = []
    n = len(lines)
    i = 0

    while i < n:
        line = lines[i].strip()
        match = re.match(surname_pattern, line)

        if not match:
            i += 1
            continue

        surname = match.group(1)

        # ищем телефон в ближайших SEARCH_RANGE строках
        for j in range(i + 1, min(i + 1 + SEARCH_RANGE, n)):
            if not lines[j].startswith("Номер телефона или email:"):
                continue

            value = lines[j].split(":", 1)[1].strip()

            if re.match(phone_pattern, value):
                formatted = format_phone_number(value, clean_pattern)
                result.append((surname, formatted))
            break

        i += 1

    return result