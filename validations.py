# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D
import re
import calendar


def is_valid_date(date: str) -> bool:
    """Check date"""
    if not (re.fullmatch(r"\d{1,2}[/.-]\d{1,2}[/.-]\d{4}", date)):
        return False
    day, month, year = map(int, re.split(r"[/.-]+", date))
    if not 1 <= month <= 12:
        return False
    elif not (1 <= day <= calendar.monthrange(year, month)[1] and 1900 <= year <= 2025):
        return False
    return True


def is_valid_phone(phone: str) -> bool:
    """Check phone"""
    if not (
        re.fullmatch(r"8 [(]?\d{3}[)]? \d{3}[\s-]\d{2}[\s-]\d{2}", phone)
        or re.fullmatch(r"[+]7 [(]?\d{3}[)]? \d{3}[\s-]\d{2}[\s-]\d{2}", phone)
        or re.fullmatch(r"[+]7\d{10}", phone)
        or re.fullmatch(r"8\d{10}", phone)
    ):
        return False
    return True


def is_valid_email(email: str) -> bool:
    """Check email"""
    if "@" not in email:
        return False
    if not email[email.find("@") + 1 :] in ["gmail.com", "mail.ru", "yandex.ru"]:
        return False
    if not re.fullmatch(r"[A-Za-z0-9._%+-]{,64}", email[: email.find("@")]):
        return False

    return True


def is_valid_userdata(userdata: list[list[str]]) -> bool:
    """Check UserData collection"""
    if userdata[0][0].islower() or userdata[1][0].islower():
        return False
    if userdata[2] not in [
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
    if not is_valid_date(userdata[3]):
        return False
    if not (is_valid_phone(userdata[4]) or is_valid_email(userdata[4])):
        return False
    return True
