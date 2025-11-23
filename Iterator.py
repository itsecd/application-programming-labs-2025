import csv

class CSVIterator:
    """ Итератор. Просто итератор."""
    def __init__(self, data: list[dict]):
        self.csv_data = data
        self.limit = len(data)
        self.counter = 0
        
    
    @classmethod
    def fromfilename(cls, source_file: str):
        """ Метод класса для создания объектов из файлов"""
        with open(source_file, mode="r", encoding="utf-8") as f:
            csv_data = list(csv.DictReader(f))
        return cls(csv_data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= self.limit:
            raise StopIteration
        value = (self.csv_data[self.counter])
        self.counter += 1
        return value
    
    def reset(self):
        self.counter = 0