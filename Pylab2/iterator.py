import os
import csv
from typing import Iterator


class AudioFileIterator:
    def __init__(self, source: str):
        self.paths = []

        if os.path.isdir(source):
            for root, _, files in os.walk(source):
                for f in files:
                    if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                        self.paths.append(os.path.join(root, f))
        elif os.path.isfile(source) and source.endswith(".csv"):
            with open(source, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "absolute_path" in row:
                        self.paths.append(row["absolute_path"])
        else:
            raise ValueError(
                "Source must be a path to a CSV file or folder")

        self._index = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self._index >= len(self.paths):
            raise StopIteration
        path = self.paths[self._index]
        self._index += 1
        return path

    def __len__(self) -> int:
        return len(self.paths)