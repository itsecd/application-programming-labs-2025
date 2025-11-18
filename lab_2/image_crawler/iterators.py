import csv
import os
from pathlib import Path
from typing import Iterator, List


class ImagePathIterator:
    """Итератор по путям к изображениям из CSV или папки."""

    def __init__(self, source: str) -> None:
        self.paths: List[str] = []

        if os.path.isfile(source) and source.endswith('.csv'):
            with open(source, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.paths = [row['absolute_path'] for row in reader]
        elif os.path.isdir(source):
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            self.paths = [
                str(Path(source) / f)
                for f in os.listdir(source)
                if Path(f).suffix.lower() in image_extensions
            ]
        else:
            raise ValueError("Источник должен быть CSV-файлом или папкой")

        self.index = 0

    def __iter__(self) -> Iterator[str]:
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        return len(self.paths)
