

import csv
import os
from typing import Iterator, Union, List

class FileIterator:
    """
    Итератор по путям к файлам. Принимает либо путь к CSV-файлу аннотаций,
    либо путь к папке с изображениями.
    """

    def __init__(self, source: str):
        """
        Инициализирует итератор.

        Args:
            source (str): Путь к файлу аннотаций (.csv) или к папке с изображениями.

        Raises:
            FileNotFoundError: Если источник не существует.
            ValueError: Если источник не является ни файлом, ни папкой.
        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"Источник не найден: {source}")

        self.source = source
        self.file_paths: List[str] = []

        if source.endswith('.csv'):
            self._load_from_csv()
        elif os.path.isdir(source):
            self._load_from_directory()
        else:
            raise ValueError(f"Источник должен быть .csv файлом или директорией: {source}")

    def _load_from_csv(self) -> None:
        """Загружает пути из CSV-файла."""
        try:
            with open(self.source, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'absolute_path' in row:
                        self.file_paths.append(row['absolute_path'])
        except Exception as e:
            raise RuntimeError(f"Ошибка чтения CSV: {e}")

    def _load_from_directory(self) -> None:
        """Загружает пути из директории."""
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
        for filename in os.listdir(self.source):
            filepath = os.path.join(self.source, filename)
            if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in image_extensions:
                self.file_paths.append(os.path.abspath(filepath))

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор по списку путей."""
        return iter(self.file_paths)

    def __len__(self) -> int:
        """Возвращает количество файлов."""
        return len(self.file_paths)

    def __repr__(self) -> str:
        return f"<FileIterator(source='{self.source}', count={len(self.file_paths)} files)>"