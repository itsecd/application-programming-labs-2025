import argparse
import re

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
        leap = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
        max_day = 29 if leap else 28
    else:
        max_day = days_in_month[month]

    return day <= max_day

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Путь до файла с данными")
    args = parser.parse_args()

    with open(args.filename, "r", encoding="utf-8") as f:
        content = f.read()

    raw_records = content.split("\n\n")
    records = [rec.split("\n") for rec in raw_records]

    invalid_records = []
    valid_records = []

    for rec in records:
        dob_line = next((line for line in rec if line.startswith("Дата рождения")), None)
        if not dob_line:
            continue
        dob = dob_line.split(":", 1)[1].strip()

        if not date_check(dob):
            invalid_records.append(rec)
        else:
            valid_records.append(rec)

    print("Анкеты с некорректной датой рождения")
    for rec in invalid_records:
        print("\n".join(rec))

    with open("output.txt", "w", encoding="utf-8") as f:
        for rec in valid_records:
            f.write("\n".join(rec) + "\n\n")

    print(f"\nОбщее количество некорректных анкет {len(invalid_records)}")
    print(f" Результат сохранён в файл output.txt")

if __name__ == "__main__":
    main()
