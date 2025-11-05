import re 

from person import Person
from validator import Validator


class Parser:
    """
    Класс для парсинга блоков данных о людях из текстового файла.
    Позволяет читать файл, извлекать данные, валидировать и сохранять результат.
    """

    def __init__(self, filepath: str):
        """
        Инициализирует объект парсера.

        :param filepath: Путь к файлу, который нужно обработать.
        """
        self.filepath = filepath
        self.people = []

    def read_file(self) -> str:
        """
        Безопасно читает содержимое файла и возвращает его как строку.

        :return: Содержимое файла в виде строки.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise IOError(f"File open error '{self.filepath}': {e}")

    def parse(self):
        """
        Разбирает содержимое файла, выделяя блоки с данными людей.
        """
        data = self.read_file()
        blocks = re.split(r"\d+\)\s*\n", data)
        for block in blocks:
            if block:
                self.people.append(self.parse_person(block))

    @staticmethod
    def parse_person(text: str) -> Person:
        """
        Извлекает информацию о человеке из текстового блока и возвращает объект Person.

        :param text: Текстовый блок с данными одного человека.
        :return: Объект Person с заполненными полями.
        """

        def find(pattern: str) -> str:
            """Ищет совпадение по шаблону и возвращает найденное значение или '-'."""
            m = re.search(pattern, text)
            return m.group(1).strip() if m else "-"

        surname = Validator.validate_name(find(r"Фамилия:\s*(.+)"))
        name = Validator.validate_name(find(r"Имя:\s*(.+)"))
        gender = Validator.validate_gender(find(r"Пол:\s*(.+)"))
        birth = Validator.validate_date(find(r"Дата рождения:\s*(.+)"))
        contact = Validator.validate_contact(find(r"Номер телефона или email:\s*(.+)"))
        city = Validator.validate_city(find(r"Город:\s*(.+)"))

        return Person(surname, name, gender, birth, contact, city)

    def save(self, output_file: str = "output.txt"):
        """
        Сохраняет обработанные данные о людях в выходной файл.

        :param output_file: Имя файла для сохранения результатов.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            for person in self.people:
                f.write(str(person) + "\n")

