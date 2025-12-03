import csv
import os
from typing import List


def create_annotation_csv(folder_path: str, csv_path: str) -> None:
    """
    Создаёт CSV-файл с аннотацией (абсолютные и относительные пути к изображениям).

    :param folder_path: Папка с изображениями.
    :param csv_path: Путь к создаваемому CSV-файлу.
    """
    image_files: List[str] = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Абсолютный путь", "Относительный путь"])

        for filename in image_files:
            abs_path = os.path.abspath(os.path.join(folder_path, filename))
            rel_path = os.path.relpath(abs_path, start=os.getcwd())
            writer.writerow([abs_path, rel_path])

    print(f"Файл-аннотация создан: {os.path.abspath(csv_path)}")
