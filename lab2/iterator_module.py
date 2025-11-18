import csv


class FileIterator:
    """
    Итератор для обхода путей из CSV-файла аннотации.
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._rows = []
        self._index = 0

        try:
            with open(csv_path, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                self._rows = [row[0] for row in reader if row]
        except FileNotFoundError:
            print(f"Файл аннотации не найден: {csv_path}")
            self._rows = []

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self._index >= len(self._rows):
            raise StopIteration

        path = self._rows[self._index]
        self._index += 1
        return path
