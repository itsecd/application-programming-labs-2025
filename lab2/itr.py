import csv


class SoundtrackIterator:
    """Итератор для построчного чтения CSV с аннотациями."""
    
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            self._rows = list(csv.DictReader(file))
        self._index = 0
        self._total = len(self._rows)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self._total:
            raise StopIteration
        
        row = self._rows[self._index]
        self._index += 1
        return row
