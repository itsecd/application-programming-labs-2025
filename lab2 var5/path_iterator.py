
from pathlib import Path
from typing import Optional, Iterator


class ImagePathIterator:
    """Итератор по путям к файлам."""
    def __init__(self, *, annotation_file=None, folder_path=None):
        if annotation_file is None and folder_path is None:
            raise ValueError("Нужно задать хотя бы один аргумент: файл аннотаций или путь к папке.")
        if annotation_file is not None and folder_path is not None:
            raise ValueError("Нельзя одновременно передавать файл аннотаций и путь к папке.")

        self.paths = []
        if annotation_file is not None:
            with open(annotation_file, 'r') as f:
                next(f)  # Пропустить заголовочную строку
                self.paths = [line.strip().split(',')[0] for line in f]
        elif folder_path is not None:
            folder = Path(folder_path)
            self.paths = [str(p.relative_to(folder)) for p in folder.glob('*')]

    def __iter__(self):
        return iter(self.paths)