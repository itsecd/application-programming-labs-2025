import csv
from collections.abc import Iterator


class ImageIterator:
    """
    Simple iterator to read CSV annotations and return absolute paths.
    """

    def __init__(self, annotation_path: str) -> None:
        """
        Constructor.
        """
        self.annotation_path = annotation_path
        self.paths = []
        self.counter = 0

        try:
            with open(self.annotation_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row:
                        self.paths.append(row[0])
        except FileNotFoundError:
            print(f"No CSV file by path: {self.annotation_path}")
        except Exception as e:
            print(f"Error while working with CSV file: {e}")

    def __iter__(self) -> Iterator:
        """
        Returns the iterator object itself.
        """
        return self

    def __next__(self) -> str:
        """
        Returns the next path from the list.
        """
        if self.counter < len(self.paths):
            path = self.paths[self.counter]
            self.counter += 1
            return path
        else:
            raise StopIteration
