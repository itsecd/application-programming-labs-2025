import csv
from pathlib import Path


class ImagePathIterator:
    """Итератор по путям к файлам изображений."""

    def __init__(self: str, annotation_file: str, folder_path: str)-> None:
        self.paths = []
        self.index = 0

        if annotation_file: #Если передан файл с аннотациями, то загружаем пути из CSV(Comma-separated Values-значения,разделенные заятыми)
            self._load_from_csv(annotation_file)
        elif folder_path: #Если не передан CSV, но передана папка сканируем папку на изображения
            self._load_from_folder(folder_path)

    def _load_from_csv(self: str, annotation_file: str)-> None:
        """Загружает пути из CSV файла."""
        try:
            with open(annotation_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.paths.append(row[0])
        except Exception as e:
            raise Exception (f"Error reading CSV: {e}")

    def _load_from_folder(self: str, folder_path: str)-> None:
        """Загружает пути из папки."""
        folder = Path(folder_path)
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            for img_path in folder.rglob(ext):
                self.paths.append(str(img_path.absolute()))

    def __iter__(self: str)-> None:
        return self

    def __next__(self: str)-> None:
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration
