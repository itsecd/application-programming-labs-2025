'''
Итератор по путям файлов из CSV-аннотации 
'''
import csv
from pathlib import Path

class FilePathIterator:
    """Итератор по путям файлов из CSV-аннотации.
        
        annotation_file: Путь к CSV-файлу аннотации.
        rows: Список строк из CSV-файла.
        _index: Текущий индекс при переборе.

    """

    def __init__(self, annotation_file: str) -> None:
        """
        Инициализация итератора.

        :param annotation_file: Путь к CSV-файлу аннотации.
        :raises FileNotFoundError: Если файл не существует.
        """
        self.annotation_file = Path(annotation_file)
        self.rows: list[dict] = []

        if not self.annotation_file.exists():
            raise FileNotFoundError(
                f"Аннотация не найдена: {annotation_file}"
            )

        try:
            with open(
                self.annotation_file, 'r', encoding='utf-8'
            ) as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)

        except FileNotFoundError:
            print(f"Файл {annotation_file} не найден")
            self.rows = []
        except OSError as e:
            print(f"Ошибка чтения файла '{annotation_file}': {e}")
            self.rows = []
        self._index: int = 0

    def __iter__(self):
        """Начало итерации."""
        self._index = 0
        return self

    def __next__(self) -> tuple[str, str, str]:
        """
        Получить следующую строку.
        :return: Кортеж (filename, abs_path, rel_path).
        :raises StopIteration: Когда не осталось строк.
        """
        if self._index >= len(self.rows):
            raise StopIteration

        row = self.rows[self._index]
        self._index += 1

        return (
            row.get('Filename', ''),
            row.get('Absolute Path', ''),
            row.get('Relative Path', '')
        )
