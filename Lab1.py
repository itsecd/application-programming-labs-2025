import argparse
import re
import calendar

DATE_PATTERN = re.compile(r"Дата рождения\s*:\s*(\d{1,2}[./-]\d{1,2}[./-]\d{4})")

def date_check(date: str) -> bool:
    """Проверка корректности даты (с учетом високосных годов)"""
    if not re.fullmatch(r"\d{1,2}([./-])\d{1,2}\1\d{4}", date):
        return False

    day, month, year = map(int, re.split(r"[./-]", date))

    if not (1900 <= year <= 2025 and 1 <= month <= 12 and 1 <= day <= 31):
        return False
    
    days_in_month = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    if month == 2:
        if calendar.isleap(year):
            max_day=29
        else:
            max_day=28
    else:
        max_day = days_in_month[month]

    return day <= max_day

def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def parse_records(content: str):
    raw_records = content.strip().split("\n\n")
    return [rec.split("\n") for rec in raw_records]

def extract_dob(record: list[str]) -> str | None:
    """Ищет строку с датой рождения через regex"""
    for line in record:
        match = DATE_PATTERN.match(line)
        if match:
            return match.group(1)
    return None

def validate_records(records):
    invalid_records, valid_records = [], []
    for rec in records:
        dob = extract_dob(rec)
        if dob and date_check(dob):
            valid_records.append(rec)
        else:
            invalid_records.append(rec)
    return invalid_records, valid_records

def print_file(invalid_records,valid_records):
    print("Анкеты с некорректной датой рождения")
    for rec in invalid_records:
        print("\n".join(rec))

    with open("output.txt", "w", encoding="utf-8") as f:
        for rec in valid_records:
            f.write("\n".join(rec) + "\n\n")

    print(f"\nОбщее количество некорректных анкет {len(invalid_records)}")
    print(f"Результат сохранён в файл output.txt")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Путь до файла с данными")
    args = parser.parse_args()
    content = read_file(args.filename)
    records = parse_records(content)
    invalid_records, valid_records = validate_records(records)
    print_file(invalid_records, valid_records)


if __name__ == "__main__":
    main()
