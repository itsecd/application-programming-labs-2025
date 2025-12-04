"""
Итератор для датасета изображений из лабораторной работы №2.
"""

import csv
import os


class DatasetIterator:
    """Итератор для работы с датасетом изображений."""

    def __init__(self, annotation_file: str = None, folder_path: str = None) -> None:
        """Инициализация итератора.
        
        Args:
            annotation_file: Путь к файлу аннотации CSV
            folder_path: Путь к папке с изображениями
        """
        self.paths = []
        self.current_index = 0

        if annotation_file:
            self._load_from_annotation(annotation_file)
        elif folder_path:
            self._load_from_folder(folder_path)

    def _load_from_annotation(self, annotation_file: str) -> None:
        """Загружает пути из CSV файла аннотации."""
        try:
            with open(annotation_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Пропускаем заголовок
                
                for row in reader:
                    if row:  # Если строка не пустая
                        # Предполагаем, что путь в первой колонке
                        path = row[0].strip()
                        if path and os.path.exists(path):
                            self.paths.append(path)
                        else:
                            # Если путь относительный, пробуем найти относительно аннотации
                            base_dir = os.path.dirname(annotation_file)
                            abs_path = os.path.join(base_dir, path)
                            if os.path.exists(abs_path):
                                self.paths.append(abs_path)
        except Exception as e:
            raise Exception(f"Ошибка загрузки аннотации: {e}")

    def _load_from_folder(self, folder_path: str) -> None:
        """Загружает пути напрямую из папки."""
        try:
            formats = ('.jpg', '.jpeg', '.png')
            
            for filename in sorted(os.listdir(folder_path)):
                if filename.lower().endswith(formats):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.exists(full_path):
                        self.paths.append(full_path)
        except Exception as e:
            raise Exception(f"Ошибка загрузки папки: {e}")

    def __iter__(self):
        """Возвращает итератор."""
        self.current_index = 0
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь."""
        if self.current_index < len(self.paths):
            path = self.paths[self.current_index]
            self.current_index += 1
            return path
        raise StopIteration

    def __len__(self) -> int:
        """Возвращает количество изображений."""
        return len(self.paths)

    def get_current_index(self) -> int:
        """Возвращает текущий индекс (нумерация с 1 для пользователя)."""
        return self.current_index

    def has_next(self) -> bool:
        """Проверяет наличие следующего изображения."""
        return self.current_index < len(self.paths)

    def has_previous(self) -> bool:
        """Проверяет наличие предыдущего изображения."""
        return self.current_index > 1

    def get_current_image(self) -> str:
        """Возвращает текущее изображение."""
        if 0 <= self.current_index - 1 < len(self.paths):
            return self.paths[self.current_index - 1]
        return ""