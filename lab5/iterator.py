import csv
import os
from typing import List, Iterator


class AnnotationIterator:
    """
    Итератор по CSV: берет путь к изображению из первого столбца
    """

    def __init__(self, annotation_file: str) -> None:
        if not annotation_file.endswith(".csv"):
            raise ValueError("Файл аннотации должен иметь расширение .csv")

        if not os.path.exists(annotation_file):
            raise FileNotFoundError(annotation_file)

        self.data: List[str] = []

        with open(annotation_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    self.data.append(row[0])

        if not self.data:
            raise ValueError("CSV пустой")

        self.index = 0

    def __iter__(self) -> Iterator[str]:
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value
