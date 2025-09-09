import re


def is_valid_date(date: str) -> bool:
    """Check date"""
    months = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    if not (
        re.fullmatch(r"\d\d[/.-]\d\d[/.-]\d\d\d\d", date)
        or re.fullmatch(r"\d[/.-]\d[/.-]\d\d\d\d", date)
    ):
        return False
    day, month, year = map(int, re.split(r"[/.-]+", date))
    if not 1 <= month <= 12:
        return False
    elif not (1 <= day <= months[month] and 1900 <= year <= 2025):
        return False
    return True


def is_valid_phone(phone: str) -> bool:
    """Check phone"""
    if not (
        re.fullmatch(r"8 [(]\d\d\d[)] \d\d\d[\s-]\d\d[\s-]\d\d", phone)
        or re.fullmatch(r"[+]7 [(]\d\d\d[)] \d\d\d[\s-]\d\d[\s-]\d\d", phone)
        or re.fullmatch(r"[+]7 \d\d\d \d\d\d[\s-]\d\d[\s-]\d\d", phone)
        or re.fullmatch(r"8 \d\d\d \d\d\d[\s-]\d\d[\s-]\d\d", phone)
        or re.fullmatch(r"[+]7\d\d\d\d\d\d\d\d\d\d", phone)
        or re.fullmatch(r"8\d\d\d\d\d\d\d\d\d\d", phone)
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
