import csv
import os
from pathlib import Path
from typing import Iterator, List


class ImageIterator:
    """Итератор для работы с путями к изображениям из CSV или директории"""
    
    def __init__(self, source: str) -> None:
        """Инициализирую итератор с путями к изображениям
            source: Путь к CSV файлу или директории с изображениями"""
        self.paths: List[str] = []
        self.counter: int = 0
        
        if os.path.isfile(source) and source.endswith('.csv'):
            self._load_from_csv(source)
        elif os.path.isdir(source):
            self._load_from_directory(source)
        else:
            raise ValueError("Источник должен быть CSV файлом или папкой")
    
    def _load_from_csv(self, csv_path: str) -> None:
        """Загружаю пути к изображениям из CSV файла."""
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Пробуем разные возможные колонки
                    if 'absolute_path' in row and row['absolute_path']:
                        abs_path = row['absolute_path']
                        if os.path.exists(abs_path):
                            self.paths.append(abs_path)
                    elif 'relative_path' in row and row['relative_path']:
                        rel_path = row['relative_path']
                        # Создаем абсолютный путь
                        base_dir = os.path.dirname(csv_path)
                        abs_path = os.path.join(base_dir, rel_path)
                        if os.path.exists(abs_path):
                            self.paths.append(abs_path)
        except Exception as e:
            print(f"Ошибка загрузки CSV: {e}")
            raise
    
    def _load_from_directory(self, directory: str) -> None:
        """Загружаю пути к изображениям из директории."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        try:
            for file_path in Path(directory).rglob('*'):
                if file_path.suffix.lower() in image_extensions:
                    if os.path.getsize(file_path) > 0:  # Проверяем что файл не пустой
                        self.paths.append(str(file_path))
        except Exception as e:
            print(f"Ошибка загрузки из директории: {e}")
            raise
    
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