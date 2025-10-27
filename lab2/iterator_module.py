import csv
from typing import Iterator, List


class FileIterator:
    """
    Итератор для обхода путей к изображениям из CSV-файла.
    """

    def __init__(self, csv_path: str) -> None:
        """
        Инициализация итератора.

        :param csv_path: Путь к CSV-файлу с аннотацией.
        """
        self.csv_path = csv_path
        self.paths: List[str] = self._load_paths()
        self.index = 0

    def _load_paths(self) -> List[str]:
        """Загружает пути из CSV-файла."""
        paths = []
        with open(self.csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                paths.append(row[0])
        return paths

    def __iter__(self) -> Iterator[str]:
        """Возвращает сам итератор."""
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь из списка."""
        if self.index < len(self.paths):
            result = self.paths[self.index]
            self.index += 1
            return result
        raise StopIteration
