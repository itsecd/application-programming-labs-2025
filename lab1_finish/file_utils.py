import os
from typing import List, Tuple, Optional


def read_file(filename: str) -> List[str]:
    """Читает файл и возвращает список строк"""
    try:
        if not os.path.exists(filename):
            print(f"Ошибка: Файл '{filename}' не найден.")
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []


def save_to_file(data: List[Tuple[str, str]], output_filename: Optional[str] = None) -> Optional[str]:
    """Сохраняет данные в файл в формате 'Фамилия: номер телефона'."""

    # Если пользователь не указал файл — используем файл по умолчанию
    if not output_filename:
        output_filename = "phonebook.txt"

    try:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for surname, phone in data:
                output_file.write(f"{surname}: {phone}\n")

        return output_filename

    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return None

