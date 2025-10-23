import re
import sys
import argparse
from datetime import datetime

class Person:
    def __init__(self, surname="-", name="-", gender="-", birth="-", contact="-", city="-"):
        self.surname = surname
        self.name = name
        self.gender = gender
        self.birth = birth
        self.contact = contact
        self.city = city

    def __str__(self):
        return f"{self.surname};{self.name};{self.gender};{self.birth};{self.contact};{self.city}"

class Validator:
    name_pattern = re.compile(r"^[А-ЯЁ][а-яё]+$")
    gender_pattern = re.compile(r"^(М|м|Ж|ж|Мужской|мужской|Женский|женский)$")
    date_pattern = re.compile(r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})")
    city_pattern = re.compile(r"^(?:г\.)?\s*[А-ЯЁ][А-ЯЁа-яё\s-]+$")

    phone_patterns = [
        re.compile(r"^(?:\+7|8)\s{1}\([\d]{3}\)\s{1}[\d]{3}-[\d]{2}-[\d]{2}$"),   # +7 (777) 777-77-77
        re.compile(r"^(?:\+7|8)\d{10}$"),                                         # +77777777777
        re.compile(r"^(?:\+7|8)\s{1}\d{3}\s{1}\d{3}[-]{1}\d{2}[-]{1}\d{2}$"),     # +7 777 777-77-77
        re.compile(r"^(?:\+7|8)\s{1}\(\d{3}\)\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}$"),   # +7 (777) 777 77 77
        re.compile(r"^(?:\+7|8)\s{1}\d{3}\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}$"),       # +7 777 777 77 77
    ]

    email_pattern = re.compile(r"^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$")

    @staticmethod
    def validate_name(value: str) -> str:
        value = value.strip()
        return value if Validator.name_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_gender(value: str) -> str:
        value = value.strip()
        return value if Validator.gender_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_date(value: str) -> str:
        match = Validator.date_pattern.fullmatch(value.strip())
        if not match:
            return "-"
        day, month, year = map(int, match.groups())
        try:
            if 1900 <= year <= datetime.now().year:
                dt = datetime(year, month, day)
                return dt.strftime("%d.%m.%Y")
        except ValueError:
            pass
        return "-"

    @staticmethod
    def validate_contact(value: str) -> str:
        value = value.strip()

        for pattern in Validator.phone_patterns:
            if pattern.fullmatch(value):
                digits = re.sub(r"\D", "", value)

                # 8XXXXXXXXXX || 7XXXXXXXXXX
                phone = digits[1:]

                return f"+7 {phone[:3]} {phone[3:6]}-{phone[6:8]}-{phone[8:]}"

        # email?
        return value if Validator.email_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_city(value: str) -> str:
        value = value.strip()
        if Validator.city_pattern.fullmatch(value):
            if not value.startswith("г."):
                return f"г. {value}"
            return value
        return "-"

class PeopleParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.people = []

    def parse(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = f.read().strip()
        
        # split "\d)\n"
        blocks = re.split(r"\d+\)\s*\n", data)
        for block in blocks:
            if block:
                self.people.append(self.parse_person(block))

    @staticmethod
    def parse_person(text: str):
        def find(pattern):
            m = re.search(pattern, text)
            return m.group(1).strip() if m else "-"

        surname = Validator.validate_name(find(r"Фамилия:\s*(.+)"))
        name = Validator.validate_name(find(r"Имя:\s*(.+)"))
        gender = Validator.validate_gender(find(r"Пол:\s*(.+)"))
        birth = Validator.validate_date(find(r"Дата рождения:\s*(.+)"))
        contact = Validator.validate_contact(find(r"Номер телефона или email:\s*(.+)"))
        city = Validator.validate_city(find(r"Город:\s*(.+)"))

        return Person(surname, name, gender, birth, contact, city)

    def save(self, output_file="output.txt"):
        with open(output_file, "w", encoding="utf-8") as f:
            for p in self.people:
                f.write(str(p) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="path/to/data")
    args = parser.parse_args()

    processor = PeopleParser(args.filename)
    processor.parse()
    processor.save()
    print(f"Processing complete. The result is recorded in output.txt")

if __name__ == "__main__":
    main()

