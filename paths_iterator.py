import csv
import os
from pathlib import Path
from typing import Iterator, List


class ImageList:
    """Итератор по изображениям из CSV или директории."""

    def __init__(self, source: str) -> None:
        self.items: List[str] = []

        if os.path.isfile(source) and source.endswith(".csv"):
            with open(source, "r", encoding="utf-8") as f:
                rdr = csv.DictReader(f)
                self.items = [row["absolute_path"] for row in rdr]

        elif os.path.isdir(source):
            exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
            self.items = [
                str(Path(source) / name)
                for name in os.listdir(source)
                if Path(name).suffix.lower() in exts
            ]

        else:
            raise ValueError("Источник должен быть CSV-файлом или папкой")

        self.pos = 0

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