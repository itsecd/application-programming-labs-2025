"""Модуль с итератором для работы с путями к аудиофайлам."""
import csv
import os
from typing import Iterator, List


class AudioFileIterator:
    """
    Итератор для работы с путями к аудиофайлам.

    Может принимать как путь к папке, так и путь к CSV файлу аннотации.
    """

    def __init__(self, source: str) -> None:
        """
        Инициализирует итератор.

        Args:
            source: Путь к папке или CSV файлу аннотации
        """
        self.paths: List[str] = []
        self._index: int = 0

        try:
            if os.path.isdir(source):
                self._load_from_directory(source)
            elif os.path.isfile(source) and source.endswith(".csv"):
                self._load_from_csv(source)
            else:
                raise ValueError(
                    "Источник должен быть путем к CSV файлу или папке"
                )
        except Exception as e:
            print(f"Ошибка при инициализации итератора: {e}")
            self.paths = []

    def _load_from_directory(self, directory_path: str) -> None:
        """Загружает пути к файлам из директории."""
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if file.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                        self.paths.append(os.path.join(root, file))
        except Exception as e:
            print(f"Ошибка при загрузке из директории: {e}")

    def _load_from_csv(self, csv_path: str) -> None:
        """Загружает пути к файлам из CSV аннотации."""
        try:
            with open(csv_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "absolute_path" in row:
                        self.paths.append(row["absolute_path"])
        except Exception as e:
            print(f"Ошибка при загрузке из CSV: {e}")

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор."""
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к файлу."""
        if self._index >= len(self.paths):
            raise StopIteration
        path = self.paths[self._index]
        self._index += 1
        return path

    def __len__(self) -> int:
        """Возвращает количество файлов."""
        return len(self.paths)