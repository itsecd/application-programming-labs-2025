"""Итератор для датасета изображений."""
import pandas as pd
import os


class DatasetIterator:
    """Итератор для навигации по датасету изображений."""
    
    def __init__(self, annotation_file=None, dataset_dir=None):
        """
        Инициализация итератора.
        
        Args:
            annotation_file: Путь к файлу аннотации CSV
            dataset_dir: Папка с изображениями
        """
        self.annotation_file = annotation_file
        self.dataset_dir = dataset_dir
        self.current_index = 0
        self.image_paths = []
        self.labels = []
        
        self._load_data()
    
    def _load_data(self):
        """Загружает данные из аннотации или папки."""
        if self.annotation_file and os.path.exists(self.annotation_file):
            # Загрузка из CSV файла
            df = pd.read_csv(self.annotation_file)
            if 'absolute_path' in df.columns and 'relative_path' in df.columns:
                self.image_paths = df['absolute_path'].tolist()
            else:
                # Если колонки называются по-другому
                self.image_paths = df.iloc[:, 1].tolist()  # Вторая колонка - абсолютные пути
        elif self.dataset_dir and os.path.exists(self.dataset_dir):
            # Загрузка из папки
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            for file in os.listdir(self.dataset_dir):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    self.image_paths.append(os.path.join(self.dataset_dir, file))
        
        # Сортируем пути для consistent порядка
        self.image_paths.sort()
    
    def __len__(self):
        """Возвращает количество изображений."""
        return len(self.image_paths)
    
    def __iter__(self):
        """Возвращает сам итератор."""
        return self
    
    def __next__(self):
        """Возвращает следующее изображение."""
        if self.current_index >= len(self.image_paths):
            raise StopIteration
        
        image_path = self.image_paths[self.current_index]
        self.current_index += 1
        return image_path
    
    def next(self):
        """Следующее изображение."""
        
        self.current_index += 1
        if self.current_index >= len(self.image_paths):
            self.current_index = 0  # Зацикливание
        return self.image_paths[self.current_index]
    
    def prev(self):
        """Предыдущее изображение."""
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.image_paths) - 1  # Зацикливание
        return self.image_paths[self.current_index]
    
    def get_current(self):
        """Текущее изображение."""
        if not self.image_paths:
            return None
        return self.image_paths[self.current_index]
    
    def get_current_index(self):
        """Текущий индекс."""
        return self.current_index
    
    def get_total_count(self):
        """Общее количество изображений."""
        return len(self.image_paths)
    
    def reset(self):
        """Сброс итератора в начало."""
        self.current_index = 0