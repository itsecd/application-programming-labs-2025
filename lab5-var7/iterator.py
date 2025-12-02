import os
import csv


class DatasetIterator:
    """
    итератор для датасета absolute_path,relative_path,color
    """

    def __init__(self, dataset_path=None, annotation_file=None):

        if dataset_path is None and annotation_file is None:
            raise ValueError("нужно указать dataset_path или annotation_file")

        if dataset_path is not None:
            if not os.path.isdir(dataset_path):
                raise NotADirectoryError(f"папка не найдена: {dataset_path}")
            csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]
            if not csv_files:
                raise FileNotFoundError("в папке не найден файл аннотаций (*.csv)")
            annotation_file = os.path.join(dataset_path, csv_files[0])


        if not os.path.exists(annotation_file):
            raise FileNotFoundError(f"файл аннотаций не найден: {annotation_file}")

        self.data = self._load_csv(annotation_file)
        self.index = 0


    def _load_csv(self, file_path):
        """
        загрузка csv файла с аннотацией
        """
        rows = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)

            for row in reader:
                if len(row) < 3:
                    continue

                abs_path, rel_path, color = row

                abs_path = abs_path.replace("\\", "/")

                rows.append((abs_path, rel_path, color))

        if not rows:
            raise ValueError("csv пустой или имеет неправильный формат")

        return rows


    def __iter__(self):
        self.index = 0
        return self


    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration

        item = self.data[self.index]
        self.index += 1
        return item

    def prev(self):

        if self.index <= 1:
            raise IndexError("назад больше нельзя")

        self.index -= 2
        return self.__next__()
