import csv
from typing import Iterator, List


class Iterator:
    def __init__(self, csv_path: str) -> None:
        self.csv_path = csv_path 
        self.paths = self.paths_get()  
        self.index = 0




    def __next__(self) -> str:
        if self.index < len(self.paths):

            res = self.paths[self.index]
            self.index += 1
            return res
        raise StopIteration


    def __iter__(self) -> Iterator[str]:
        return self


    def paths_get(self) -> List[str]:
        """get path"""


        paths = []
        
        with open(self.csv_path, newline='', encoding='utf-8-sig') as file:
            r = csv.reader(file)

            next(r)
            for row in r:
                paths.append(row[0])

        return paths