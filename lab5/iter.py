import csv


class SoundtrackIterator:
    """Итератор для построчного чтения"""

    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            self._rows = list(csv.DictReader(file))
        self._ind = 0
        self._total = len(self._rows)

    def __iter__(self):
        return self

    def __next__(self):
        if self._ind < self._total:
            row = self._rows[self._ind]
            self._ind += 1
            return row
        else:
            raise StopIteration