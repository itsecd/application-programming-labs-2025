import csv
import os


class AnnotationManager:
    """
    Класс для создания CSV файлов с аннотациями изображений.
    Аннотации содержат абсолютные и относительные пути к файлам.
    """

    def create_annotation(self, images_dir, annotation_file):
        """
        Создает CSV файл с путями ко всем изображениям в папке.

        Args:
            images_dir: папка с изображениями
            annotation_file: путь к CSV файлу для сохранения аннотаций

        Returns:
            Количество записанных в аннотацию изображений
        """
        image_paths = self.get_image_paths(images_dir)

        # Создаем директорию для файла аннотации, если она указана
        annotation_dir = os.path.dirname(annotation_file)
        if annotation_dir and not os.path.exists(annotation_dir):
            os.makedirs(annotation_dir)

        # Создаем CSV файл с аннотациями
        with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['absolute_path', 'relative_path'])
            writer.writerows(image_paths)

        print(f"Создана аннотация с {len(image_paths)} записями")
        return len(image_paths)

    def get_image_paths(self, directory):
        """
        Собирает все изображения из папки и возвращает их пути.

        Returns:
            Список кортежей (абсолютный_путь, относительный_путь)
        """
        image_paths = []

        if not os.path.exists(directory):
            return image_paths

        for filename in os.listdir(directory):
            if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                abs_path = os.path.abspath(os.path.join(directory, filename))
                rel_path = os.path.join(directory, filename)
                image_paths.append((abs_path, rel_path))

        return image_paths


class ImageIterator:
    """
    Итератор для удобного перебора изображений.
    Может загружать пути из CSV аннотации или напрямую из папки.
    """

    def __init__(self, annotation_file=None, folder_path=None):
        """
        Инициализирует итератор.

        Args:
            annotation_file: путь к CSV файлу с аннотациями
            folder_path: путь к папке с изображениями
        """
        self.paths = []
        self.index = 0

        if annotation_file and os.path.exists(annotation_file):
            self.load_from_annotation(annotation_file)
        elif folder_path and os.path.exists(folder_path):
            self.load_from_folder(folder_path)

    def load_from_annotation(self, annotation_file):
        """Загружает пути к изображениям из CSV файла аннотации."""
        with open(annotation_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'absolute_path' in row and os.path.exists(row['absolute_path']):
                    self.paths.append(row['absolute_path'])
        print(f"Загружено {len(self.paths)} путей из аннотации")

    def load_from_folder(self, folder_path):
        """Загружает пути к изображениям напрямую из папки."""
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                full_path = os.path.abspath(os.path.join(folder_path, filename))
                if os.path.exists(full_path):
                    self.paths.append(full_path)
        print(f"Загружено {len(self.paths)} путей из папки")

    def __iter__(self):
        """
        Возвращает сам объект как итератор.
        Сбрасывает счетчик перед началом итерации.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Возвращает следующий путь к изображению.
        Вызывается на каждой итерации цикла for.
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration

    def __len__(self):
        """Возвращает количество доступных путей к изображениям."""
        return len(self.paths)