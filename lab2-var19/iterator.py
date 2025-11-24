import csv
import os
from typing import Iterator, Tuple


class SoundFileIterator:
    """
    Итератор для перебора путей к звуковым файлам из CSV аннотации
    """

    def __init__(self, annotation_file: str) -> None:
        """
        Инициализация итератора

        Args:
            annotation_file: Путь к файлу аннотации CSV
        """
        self.annotation_file = annotation_file
        self.data = []
        self.index = 0

        try:
            with open(annotation_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Пропускаем заголовок
                self.data = [row for row in reader]
        except FileNotFoundError:
            print(f"Файл аннотации не найден: {annotation_file}")
        except Exception as e:
            print(f"Ошибка при чтении файла аннотации: {e}")

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """
        Возвращает сам объект как итератор
        """
        self.index = 0
        return self

    def __next__(self) -> Tuple[str, str]:
        """
        Возвращает следующий элемент (абсолютный путь, относительный путь)

        Returns:
            Кортеж с абсолютным и относительным путями

        Raises:
            StopIteration: когда элементы закончились
        """
        if self.index < len(self.data):
            result = tuple(self.data[self.index])
            self.index += 1
            return result
        else:
            raise StopIteration

    def __len__(self) -> int:
        """
        Возвращает количество элементов
        """
        return len(self.data)