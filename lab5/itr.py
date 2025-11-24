import csv
from typing import Dict, Optional


class SoundtrackIterator:
    """Итератор для работы с аннотацией треков."""

    def __init__(self, filename: str) -> None:
        """Инициализация итератора и чтение CSV."""
        with open(filename, "r", encoding="utf-8") as file:
            self._rows = list(csv.DictReader(file))
        self._index = 0
        self._total = len(self._rows)


    def __iter__(self):
        return self


    def __next__(self) -> Optional[Dict[str, str]]:
        """Возврат следующей строки, если есть."""
        if self._index >= self._total:
            raise StopIteration
        row = self._rows[self._index]
        self._index += 1
        return row


    def previous(self) -> Optional[Dict[str, str]]:
        """Возврат предыдущего трека и уменьшение индекса."""
        if self._index <= 1:
            return None
        self._index -= 1
        return self._rows[self._index - 1]


    def length(self) -> int:
        """Возврат общего количества треков."""
        return self._total
