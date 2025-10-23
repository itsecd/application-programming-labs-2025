import csv

class CSVIterator:
    """ Итератор. Просто итератор."""
    def __init__(self, source_file: str):
        with open(source_file, mode="r", encoding="utf-8") as f:
            self.csv_data = list(csv.DictReader(f))
        self.limit = len(self.csv_data)
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= self.limit:
            raise StopIteration
        value = (self.csv_data[self.counter])
        self.counter += 1
        return value
            