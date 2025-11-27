import csv
import os
from typing import Iterator, Optional


class DatasetIterator:
    """Итератор для работы с датасетом изображений."""

    def __init__(self, annotation_file: Optional[str] = None,
                 folder_path: Optional[str] = None) -> None:
        """Инициализация итератора."""
        self.paths = []
        self.current_index = 0

        if annotation_file and os.path.exists(annotation_file):
            self._load_from_annotation(annotation_file)
        elif folder_path and os.path.exists(folder_path):
            self._load_from_folder(folder_path)

    def _load_from_annotation(self, annotation_file: str) -> None:
        """Загружает пути из CSV файла аннотации."""
        with open(annotation_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Пробуем все возможные варианты колонок
                possible_paths = []
                
                for col_name in ['absolute_path', 'relative_path', 'path', 'file_path']:
                    if col_name in row and row[col_name]:
                        path = row[col_name].strip()
                        if path:
                            possible_paths.append((col_name, path))
                
                # Обрабатываем найденные пути
                for col_name, path in possible_paths:
                    if col_name == 'relative_path':
                        base_dir = os.path.dirname(annotation_file)
                        abs_path = os.path.abspath(os.path.join(base_dir, path))
                    else:
                        abs_path = os.path.abspath(path)
                    
                    if os.path.exists(abs_path):
                        self.paths.append(abs_path)
                        break

    def _load_from_folder(self, folder_path: str) -> None:
        """Загружает пути напрямую из папки."""
        formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in formats):
                full_path = os.path.join(folder_path, filename)
                if os.path.exists(full_path):
                    self.paths.append(full_path)

    def __iter__(self) -> Iterator[str]:
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
        """Возвращает текущий индекс."""
        return self.current_index

    def has_next(self) -> bool:
        """Проверяет наличие следующего изображения."""
        return self.current_index < len(self.paths)

    def has_previous(self) -> bool:
        """Проверяет наличие предыдущего изображения."""
        return self.current_index > 1

    def get_previous_image(self) -> Optional[str]:
        """Возвращает предыдущее изображение."""
        if self.has_previous():
            return self.paths[self.current_index - 2]
        return None

    def reset(self) -> None:
        """Сбрасывает итератор."""
        self.current_index = 0