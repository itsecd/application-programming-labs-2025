import argparse
import csv
import os
from pathlib import Path
from icrawler.builtin import BingImageCrawler 

class ImageIterator:
    """Итератор для перебора путей к изображениям"""
    def __init__(self, annotation_file=None, image_dir=None):
        if annotation_file:
            self.paths = self._load_from_annotation(annotation_file)
        elif image_dir:
            self.paths = self._load_from_directory(image_dir)
        else:
            raise ValueError("Необходимо указать либо файл аннотации, либо папку с изображениями")
        
        self.index = 0
    
    def _load_from_annotation(self, annotation_file):
        """Загрузка путей из CSV файла"""
        paths = []
        with open(annotation_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                paths.append(row[0])  # Берем абсолютный путь
        return paths
    
    def _load_from_directory(self, image_dir):
        """Загрузка путей из директории"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        paths = []
        for file_path in Path(image_dir).rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                paths.append(str(file_path.absolute()))
        return paths
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration

def download_images(keyword, output_dir, total_images, size_ranges):
    """Скачивание изображений с фильтрацией по размерам"""
    os.makedirs(output_dir, exist_ok=True)
     
    images_per_range = total_images // len(size_ranges)
    
    for i, size_range in enumerate(size_ranges):
        range_dir = os.path.join(output_dir, f"range_{i+1}")
        os.makedirs(range_dir, exist_ok=True)
        
        crawler = BingImageCrawler(storage={'root_dir': range_dir}, downloader_threads=4)
        
        # Фильтр по размеру
        filters = {
            'size': size_range,
            'type': 'photo'
        }
        
        crawler.crawl(
            keyword=keyword,
            filters=filters,
            max_num=images_per_range,
            file_idx_offset=0
        )

def create_annotation(output_dir, annotation_file):
    """Создание CSV аннотации"""
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Абсолютный путь', 'Относительный путь'])
        
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    abs_path = os.path.abspath(os.path.join(root, file))
                    rel_path = os.path.relpath(abs_path)
                    writer.writerow([abs_path, rel_path])

def main():
    parser = argparse.ArgumentParser(description='Скачивание изображений и создание аннотации')
    parser.add_argument('--output', '-o', required=True, help='Путь к папке для сохранения изображений')
    parser.add_argument('--annotation', '-a', required=True, help='Путь к файлу аннотации')
    parser.add_argument('--keyword', '-k', default='rabbit', help='Ключевое слово для поиска')
    parser.add_argument('--total', '-t', type=int, default=100, help='Общее количество изображений')
    parser.add_argument('--ranges', '-r', nargs='+', required=True, help='Диапазоны размеров в формате "large medium small"')
    
    args = parser.parse_args()
    
    # Скачивание изображений
    download_images(args.keyword, args.output, args.total, args.ranges)
    
    # Создание аннотации
    create_annotation(args.output, args.annotation)
    
    # Демонстрация работы итератора
    print("Демонстрация работы итератора (первые 5 путей):")
    iterator = ImageIterator(annotation_file=args.annotation)
    for i, path in enumerate(iterator):
        if i >= 5:
            break
        print(f"{i+1}. {path}")

if __name__ == "__main__":
    main()