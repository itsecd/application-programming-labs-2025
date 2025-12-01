from __future__ import annotations
import csv
import os
from pathlib import Path
from typing import Iterator, Dict, List, Optional


class ImageIterator:
    """
    Итератор по изображениям, загружаемый либо из CSV-аннотации,
    либо из директории.

    Атрибуты:
        data: список [absolute_path, relative_path]
        index: позиция текущего элемента
    """

    def __init__(self, annotation_file: Optional[str] = None, folder: Optional[str] = None) -> None:
        self.data: List[List[str]] = []
        if annotation_file:
            self.load_from_csv(annotation_file)
        elif folder:
            self.load_from_folder(folder)
        self.index: int = 0

    def load_from_csv(self, annotation_file: str) -> None:
        """Загружает пути изображений из CSV."""
        if os.path.exists(annotation_file):
            with open(annotation_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                self.data = [row for row in reader]

    def load_from_folder(self, folder: str) -> None:
        """Сканирует директорию и сохраняет абсолютные и относительные пути."""
        folder_path = Path(folder)
        for file_path in folder_path.rglob("*.*"):
            if file_path.is_file():
                self.data.append([str(file_path.absolute()), str(file_path.relative_to(folder_path))])

    def __iter__(self) -> Iterator[Dict[str, str]]:
        return self

    def __next__(self) -> Dict[str, str]:
        if self.index < len(self.data):
            row = self.data[self.index]
            self.index += 1
            return {"absolute_path": row[0], "relative_path": row[1]}
        raise StopIteration