import csv
import os
from typing import Union, Iterator
from pathlib import Path


class ImageIterator:
    """Итератор для перебора путей к изображениям из CSV-аннотации или директории.
    
    Args:
        annotation_source: Путь к CSV-файлу или директории с изображениями
    
    Attributes:
        paths: Список путей к изображениям
        index: Текущий индекс итерации
    """
    
    def __init__(self, annotation_source: Union[str, Path]) -> None:
        self.paths: list[str] = []
        self.index: int = 0
        
        annotation_source = Path(annotation_source)
        
        if annotation_source.is_file() and annotation_source.suffix == '.csv':
            self._read_from_csv(annotation_source)
        elif annotation_source.is_dir():
            self._read_from_directory(annotation_source)
        else:
            raise ValueError(
                f"Источник должен быть CSV-файлом или директорией. "
                f"Получено: {annotation_source}"
            )

    def _read_from_csv(self, csv_path: Path) -> None:
        """Чтение путей изображений из CSV-файла.
        
        Args:
            csv_path: Путь к CSV-файлу
        """
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'absolute_path' in row:
                        self.paths.append(row['absolute_path'])
        except Exception as e:
            raise

    def _read_from_directory(self, directory: Path) -> None:
        """Рекурсивное чтение путей изображений из директории.
        
        Args:
            directory: Путь к директории с изображениями
        """
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    self.paths.append(str(file_path.absolute()))
        except Exception as e:
            raise

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор.
        
        Returns:
            Итератор по путям изображений
        """
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к изображению.
        
        Returns:
            Абсолютный путь к изображению
            
        Raises:
            StopIteration: Когда все изображения пройдены
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество изображений.
        
        Returns:
            Количество путей к изображениям
        """
        return len(self.paths)