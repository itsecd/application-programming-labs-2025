import re
from person import Person
from validator import Validator

class Parser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.people = []

    def parse(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = f.read().strip()
        except Exception as e:
            raise IOError(f"File open error '{self.filepath}': {e}")

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

