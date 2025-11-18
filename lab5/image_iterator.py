# image_iterator.py
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
        
        # Проверяем, что есть хотя бы одно изображение
        if not self.paths:
            raise ValueError("Не найдено изображений в указанном источнике")
    
    def _load_from_csv(self, csv_path: str) -> None:
        """Загружает пути к изображениям из CSV файла"""
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'absolute_path' in row and row['absolute_path']:
                    path = row['absolute_path']
                    if os.path.exists(path):
                        self.paths.append(path)
                
                elif 'relative_path' in row and row['relative_path']:
                    rel_path = row['relative_path']
                    abs_path = os.path.join(os.path.dirname(csv_path), rel_path)
                    if os.path.exists(abs_path):
                        self.paths.append(abs_path)
    
    def _load_from_directory(self, directory: str) -> None:
        """Загружает пути к изображениям из директории"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                self.paths.append(str(file_path))
        
        # Сортируем пути для consistent порядка
        self.paths.sort()
    
    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор"""
        self.counter = 0
        return self
    
    def __next__(self) -> str:
        """Возвращает следующий путь к изображению"""
        if self.counter < len(self.paths):
            path = self.paths[self.counter]
            self.counter += 1
            return path
        raise StopIteration
    
    def get_current_index(self) -> int:
        """Возвращает текущий индекс"""
        return self.counter - 1 if self.counter > 0 else 0
    
    def get_total_count(self) -> int:
        """Возвращает общее количество изображений"""
        return len(self.paths)