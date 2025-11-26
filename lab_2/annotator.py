import csv
import os
from pathlib import Path
from typing import Iterator, Tuple, List

class FileAnnotationIterator:
    """
    Итератор по файлам из CSV-аннотации.
    """

    def __init__(self, annotation_file: str):
        """
        Инициализирует итератор.

        Args:
            annotation_file (str): Путь к CSV-файлу аннотации.

        Raises:
            FileNotFoundError: Если файл аннотации не найден.
        """
        self.annotation_file = Path(annotation_file).resolve()
        if not self.annotation_file.exists():
            raise FileNotFoundError(f"Файл аннотации не найден: {self.annotation_file}")

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """
        Возвращает итератор по строкам аннотации.

        Yields:
            Tuple[str, str]: Абсолютный и относительный пути к файлу.
        """
        with open(self.annotation_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                yield row[0], row[1]

def create_annotation_csv(
    image_directory: str,
    annotation_file: str
) -> None:
    """
    Создает CSV-файл аннотации с абсолютными и относительными путями.

    Args:
        image_directory (str): Директория с изображениями.
        annotation_file (str): Путь к файлу аннотации.

    Raises:
        Exception: При ошибках записи файла.
    """
    image_directory = Path(image_directory).resolve()
    annotation_file = Path(annotation_file).resolve()

    images = []
    for root, dirs, files in os.walk(image_directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                full_path = Path(root) / file
                images.append(full_path)

    with open(annotation_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['absolute_path', 'relative_path'])
        for img_path in images:
            relative_path = img_path.relative_to(image_directory)
            writer.writerow([str(img_path), str(relative_path)])

    print(f"Аннотация сохранена в: {annotation_file}")