from typing import List, Iterator

class CSVIterator:
    """
    Iterator
    """
    def __init__(self, paths: List[str]) -> None:
        self.paths = paths
        self.index = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self.index < len(self.paths):
            item = self.paths[self.index]
            self.index += 1
            return item
        raise StopIteration

    def reset(self):
        self.index = 0
