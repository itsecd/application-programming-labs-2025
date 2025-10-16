"""
Модуль для работы с файлами и обработки текста.
"""

import re
from typing import List


def read_file(filename: str, encoding: str = "utf-8") -> str:
    """
    Читает содержимое файла.

    """
    try:
        with open(filename, "r", encoding=encoding) as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл '{filename}' не найден.") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Невозможно прочитать файл '{filename}' в кодировке {encoding}.") from e


def write_file(filename: str, lines: List[str], encoding: str = "utf-8") -> None:
    """
    Записывает список строк в файл.

    """
    try:
        with open(filename, "w", encoding=encoding) as file:
            for line in lines:
                file.write(line + "\n")
    except IOError as e:
        raise IOError(f"Ошибка записи в файл '{filename}'.") from e


def extract_and_format_names(text: str) -> List[str]:
    """
    Извлекает из текста данные в формате:
        Фамилия: Иванов
        Имя: Иван
    и преобразует их в список строк вида "Иванов И.".

    """
    pattern = r'Фамилия: [А-Я][а-я]+\nИмя: [А-Я][а-я]+'
    matches = re.findall(pattern, text)

    result = []
    for match in matches:
        surname_line, name_line = match.split('\n')
        surname = surname_line[9:]  # Убираем "Фамилия: "
        first_name = name_line[5:]  # Убираем "Имя: "
        initial = first_name[0] + '.'
        result.append(f"{surname} {initial}")

    result.sort()
    return result