import csv
import os
from typing import List, Tuple


def create_annotation_file(file_path: str, data: List[Tuple[str, str]]) -> None:
    """
    Создает CSV файл аннотации с абсолютными и относительными путями

    Args:
        file_path: Путь к файлу аннотации
        data: Список кортежей (абсолютный путь, относительный путь)
    """
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['absolute_path', 'relative_path'])
            writer.writerows(data)
        print(f"Аннотация создана: {file_path}")
    except Exception as e:
        print(f"Ошибка при создании аннотации: {e}")


def ensure_directory(directory: str) -> None:
    """
    Создает директорию, если она не существует

    Args:
        directory: Путь к директории
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Создана директория: {directory}")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")