import os
import csv
from typing import List, Iterator


class Path_Iterator:
    """
    Итератор по пути к данным.
    """
    def __init__(self, source: str) -> None:
        self.items: List[List[str]] = []
        self.counter: int = 0

        if os.path.isfile(source):
            with open(source, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        self.items.append([row[0], row[1]])
        elif os.path.isdir(source):
            for filename in os.listdir(source):
                full_path = os.path.abspath(os.path.join(source, filename))
                rel_path = os.path.relpath(full_path)
                self.items.append([full_path, rel_path])
        else:
            raise ValueError(f"Путь не существует: {source}")

    def __iter__(self) -> Iterator[List[str]]:
        return self

    def __next__(self) -> List[str]:
        if self.counter < len(self.items):
            item = self.items[self.counter]
            self.counter += 1
            return item
        else:
            raise StopIteration