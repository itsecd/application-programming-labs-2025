
import csv
import os
from typing import Iterator, List


class ImageList:
    """Итератор по изображениям из CSV или директории."""

    def __init__(self, source: str) -> None:
        self.items: List[str] = []

        if os.path.isfile(source) and source.endswith(".csv"):
            self._load_from_csv(source)
        else:
            raise ValueError("Источник должен быть CSV-файлом")

        self.pos = 0

    def _load_from_csv(self, csv_path: str) -> None:
        """Загружает пути к изображениям из CSV файла."""
        with open(csv_path, "r", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            self.items = [row["absolute_path"] for row in rdr]

    def __iter__(self) -> Iterator[str]:
        self.pos = 0
        return self

    def __next__(self) -> str:
        if self.pos >= len(self.items):
            raise StopIteration
        out = self.items[self.pos]
        self.pos += 1
        return out

    def __len__(self) -> int:
        return len(self.items)