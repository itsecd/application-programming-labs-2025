import re 
from datetime import datetime


class Validator:
    """
    Класс для проверки и нормализации пользовательских данных.
    """

    name_pattern = re.compile(r"^[А-ЯЁ][а-яё]+$")
    gender_pattern = re.compile(r"^(М|м|Ж|ж|Мужской|мужской|Женский|женский)$")
    date_pattern = re.compile(r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})")
    city_pattern = re.compile(r"^(?:г\.)?\s*[А-ЯЁ][А-ЯЁа-яё\s-]+$")
    phone_pattern = re.compile(
        r'^(?:\+7|8)'                    # код страны
        r'(?:\s?\(?\d{3}\)?\s?)'         # (XXX) или XXX
        r'\d{3}[-\s]?\d{2}[-\s]?\d{2}$'  # оставшиеся цифры
    )
    email_pattern = re.compile(
        r"^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$"
    )

    @staticmethod
    def validate_name(value: str) -> str:
        """
        Проверяет корректность имени или фамилии.

        :param value: Введённое значение.
        :return: Валидное имя/фамилия или '-' при ошибке.
        """
        value = value.strip()
        return value if Validator.name_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_gender(value: str) -> str:
        """
        Проверяет корректность значения пола.

        :param value: Введённое значение (М/Ж или Мужской/Женский).
        :return: Валидное значение или '-'.
        """
        value = value.strip()
        return value if Validator.gender_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_date(value: str) -> str:
        """
        Проверяет корректность даты рождения и форматирует её в DD.MM.YYYY.

        :param value: Строка с датой.
        :return: Отформатированная дата или '-'.
        """
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
        """
        Проверяет корректность контактной информации (телефон или email).

        :param value: Строка с телефоном или email.
        :return: Отформатированный телефон или email, либо '-'.
        """
        value = value.strip()

        if Validator.phone_pattern.fullmatch(value):
            digits = re.sub(r"\D", "", value)
            phone = digits[-10:]
            return f"+7 {phone[:3]} {phone[3:6]}-{phone[6:8]}-{phone[8:]}"

        # email?
        return value if Validator.email_pattern.fullmatch(value) else "-"

    @staticmethod
    def validate_city(value: str) -> str:
        """
        Проверяет корректность названия города.

        :param value: Название города.
        :return: Город в формате 'г. Название' или '-'.
        """
        value = value.strip()
        if Validator.city_pattern.fullmatch(value):
            if not value.startswith("г."):
                return f"г. {value}"
            return value
        return "-"

