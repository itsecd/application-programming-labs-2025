import csv
from pathlib import Path
from typing import List, Dict


class FilePathIterator:
    """
    Итератор по путям к файлам.
    """
    def __init__(self, source: Path):
        self._file_info: List[dict] = []

        if source.is_file() and source.suffix.lower() == ".csv":
            with source.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("abs_path"):
                        self._file_info.append(row)
        else:
            raise ValueError(f"Unsupported source for iterator: {source}")
        self._i = 0

    def __iter__(self) -> "FilePathIterator":
        return self

    def __next__(self) -> Dict[str, str]:  
        if self._i >= len(self._file_info):
            raise StopIteration
        data = self._file_info[self._i]
        self._i += 1
        return data