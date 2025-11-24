

import csv
import os
from typing import List, Tuple

def create_annotation_csv(
    image_dir: str,
    annotation_file: str = "annotations.csv"
) -> None:
    """
    Создаёт CSV-файл с абсолютным и относительным путями ко всем изображениям в директории.

    Args:
        image_dir (str): Путь к директории с изображениями.
        annotation_file (str): Имя CSV-файла для сохранения аннотаций.

    Raises:
        FileNotFoundError: Если директория не существует.
        Exception: При ошибках записи файла.
    """
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Директория не найдена: {image_dir}")

    
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    image_files = [
        f for f in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, f)) and
        os.path.splitext(f)[1].lower() in image_extensions
    ]

    if not image_files:
        print("⚠️ Изображения не найдены.")
        return

    try:
        with open(annotation_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["absolute_path", "relative_path"])

            for filename in image_files:
                abs_path = os.path.abspath(os.path.join(image_dir, filename))
                rel_path = os.path.relpath(abs_path, start=os.getcwd())
                writer.writerow([abs_path, rel_path])

        print(f"✅ Аннотации сохранены в: {annotation_file}")

    except Exception as e:
        print(f"❌ Ошибка при создании CSV: {e}")
        raise