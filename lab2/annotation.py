import csv
import os
from typing import List


def create_annotation(file_paths: List[str], csv_path: str) -> None:
    """
    Создаёт CSV-аннотацию для списка файлов.

    :param file_paths: список абсолютных путей к файлам
    :param csv_path: путь к CSV файлу для сохранения аннотации
    """
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])

        for path in file_paths:
            abs_path = os.path.abspath(path)
            rel_path = os.path.relpath(path)
            writer.writerow([abs_path, rel_path])
