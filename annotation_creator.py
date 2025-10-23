import csv
import os
from typing import List


def create_annotation_csv(image_paths: List[str], annotation_file: str, output_dir: str) -> None:
    """Создает CSV файл аннотации с путями к изображениям.
        image_paths: Список абсолютных путей к изображениям
        annotation_file: Путь к файлу аннотации
        output_dir: Базовая директория для относительных путей"""
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute_path', 'relative_path'])
        
        for abs_path in image_paths:
            rel_path = os.path.relpath(abs_path, output_dir)
            writer.writerow([abs_path, rel_path])