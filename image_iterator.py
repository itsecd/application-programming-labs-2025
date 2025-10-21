import csv
import os
from pathlib import Path
from typing import Iterator, List


class ImageIterator:
    """Итератор для работы с путями к изображениям из CSV или директории"""
    
    def __init__(self, source: str) -> None:
        """Инициализирует итератор с путями к изображениям"""
        self.paths: List[str] = []
        self.counter: int = 0
        
        if os.path.isfile(source) and source.endswith('.csv'):
            self._load_from_csv(source)
        elif os.path.isdir(source):
            self._load_from_directory(source)
        else:
            raise ValueError("Источник должен быть CSV файлом или папкой")
    
    def _load_from_csv(self, csv_path: str) -> None:
        """Загружаю пути к изображениям из CSV файла"""
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.paths.append(row['absolute_path'])
    
    def _load_from_directory(self, directory: str) -> None:
        """Загружаю пути к изображениям из директории"""
        image_extensions = ['.jpg', '.jpeg', '.png']
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                self.paths.append(str(file_path))
    
    def __iter__(self) -> Iterator[str]:
        """Возвращаю итератор"""
        self.counter = 0
        return self
    
    def __next__(self) -> str:
        """Возвращаю следующий путь к изображению"""
        if self.counter < len(self.paths):
            path = self.paths[self.counter]
            self.counter += 1
            return path
        raise StopIteration