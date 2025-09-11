# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D
import re
import argparse

import validations


def get_args() -> str:
    """Parsing console arguments
    Returns None if there are no arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="Set userdata filepath (-f /path/to/file.txt)"
    )
    args = parser.parse_args()

    if args.file is None:
        return None
    return args.file


def read_file(filename: str) -> str:
    """Read file and return strings
    Return None if file is not open"""
    try:
        with open(filename, "r", encoding="utf8") as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError


def get_statistics(lines: str) -> dict[str:int]:
    userdata = []
    age_statistics = {
        "Мужчины 0-17": 0,
        "Мужчины 18-64": 0,
        "Мужчины 65+": 0,
        "Женщины 0-17": 0,
        "Женщины 18-59": 0,
        "Женщины 60+": 0,
    }
    for line in lines:
        if line == "\n" or re.fullmatch(r"\d*[)]\n", line):
            continue
        line = line[line.find(":") + 2 : -1]
        if "г." in line:
            line = line[3:]
        userdata.append(line)
        if len(userdata) < 6:
            continue
        if validations.is_valid_userdata(userdata):
            age = get_age(userdata[3])
            age_statistics[get_group_type(userdata[2][0].lower(), age)] += 1
        userdata.clear()
    return age_statistics


def save_result(age_statistics: dict[str:int]) -> None:
    """Saving statistics
    Return True if the save is successful"""
    result_str = ""
    try:
        for group, count in age_statistics.items():
            result_str += f"{group}: {count}\n"
        with open("result.txt", "w", encoding="utf-8") as file:
            file.write(result_str)
    except PermissionError:
        raise PermissionError


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
