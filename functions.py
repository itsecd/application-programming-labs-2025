# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D
import re


def get_group_type(gender: str, age: int) -> str:
    """Get key for age_statistics"""
    group_type = ""
    group_type += "Мужчины " if gender == "м" else "Женщины "
    if 0 <= age <= 17:
        group_type += "0-17"
    elif 18 <= age <= 64 and gender == "м":
        group_type += "18-64"
    elif age >= 65 and gender == "м":
        group_type += "65+"
    elif 18 <= age <= 59 and gender == "ж":
        group_type += "18-59"
    else:
        group_type += "60+"
    return group_type


def get_age(date: str) -> int:
    """Calculate age from day of Birthday to 09.09.2025"""
    day, month, year = map(int, re.split(r"[/.-]+", date))
    age = 2025 - year
    age -= 1 if month > 9 or (day >= 9 and month >= 9) else 0
    return age
