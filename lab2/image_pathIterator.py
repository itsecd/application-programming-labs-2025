import csv
import os
from typing import Iterator, Union


class ImagePathIterator:
    """Итератор путей файлов"""
    
    def __init__(self, source: str) -> None:
        self.source = source
        self.current_index = 0
        self.image_paths = []
        self._load_paths()

    def _load_paths(self) -> None:
        """Загружает пути к изображениям из файла с аннотацией или папки"""
        if self.source.endswith('.csv'):
            self._load_from_annotation()
        else:
            self._load_from_directory()

    def _load_from_annotation(self) -> None:
        """Загружает пути из CSV файла аннотации"""
        try:
            with open(self.source, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    file_path = row['Absolute_path']
                    if os.path.exists(file_path):
                        self.image_paths.append(file_path)
        except FileNotFoundError:
            print(f"Файл не найден: {self.source}")
        except Exception as e:
            print(f"Ошибка при чтении: {e}")

    def _load_from_directory(self) -> None:
        """Загружает пути из папки с изображениями"""
        if os.path.exists(self.source) and os.path.isdir(self.source):
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            
            for root, dirs, files in os.walk(self.source):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        _, file_extension = os.path.splitext(file)
                        file_ext = file_extension.lower()

                        if file_ext in image_extensions:
                            abs_path = os.path.abspath(file_path)
                            self.image_paths.append(abs_path)
        else:
            print(f"Директория не найдена: {self.source}")

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор"""
        self.current_index = 0
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к изображению"""
        if self.current_index < len(self.image_paths):
            path = self.image_paths[self.current_index]
            self.current_index += 1
            return path
        else:
            raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество путей"""
        return len(self.image_paths)