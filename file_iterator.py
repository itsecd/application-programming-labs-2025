# file_iterator.py
from typing import Iterator

class FileIterator:
    """
    Итератор, читающий файл построчно.
    """
    def __init__(self: 'FileIterator', file_path: str) -> None:
        """
        Инициализирует итератор и открывает файл
        :param file_path: Путь к файлу
        """
        try:
            self.filepath = file_path
            self.file = open(file_path, 'r', encoding='utf-8')

        except FileNotFoundError:
            self.file = None
            raise FileNotFoundError(f"Файл {file_path} не найден")

    def __iter__(self: 'FileIterator') -> Iterator[str]:
        """
        Возвращает итератор строк
        """
        return self

    def __next__(self: 'FileIterator') -> str:
        """
        Возвращает следующую строку из файла
        """
        if self.file is None:
            raise StopIteration

        line = self.file.readline()

        if not line:
            self.file.close()
            self.file = None
            raise StopIteration

        return line
