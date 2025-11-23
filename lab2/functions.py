import csv
import os
from icrawler.builtin import BingImageCrawler


class ImageIterator:
    def __init__(self, annotation_file=None, folder_path=None):
        self.paths = []
        
        try:
            if annotation_file:
                # Читаем пути из CSV файла
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Пропускаем заголовок
                    for row in reader:
                        self.paths.append(row[0])  # Берем абсолютные пути
                        
            elif folder_path:
                # Читаем пути из папки
                for file in os.listdir(folder_path):
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.abspath(os.path.join(folder_path, file))
                        self.paths.append(full_path)
        except FileNotFoundError:
            print(f"Ошибка: Файл или папка не найдены")
        except Exception as e:
            print(f"Ошибка при инициализации итератора: {e}")

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


def download_images(output_dir):
    try:
        crawler = BingImageCrawler(storage={'root_dir': output_dir})
        crawler.crawl(keyword='pig', max_num=50)
    except Exception as e:
        print(f"Ошибка при скачивании изображений: {e}")
        raise


def create_annotation(annotation_file, output_dir):
    try:
        with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Абсолютный путь', 'Относительный путь'])
            
            # Записываем пути ко всем изображениям
            for file in os.listdir(output_dir):
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    abs_path = os.path.abspath(os.path.join(output_dir, file))
                    rel_path = os.path.join(output_dir, file)
                    writer.writerow([abs_path, rel_path])
    except Exception as e:
        print(f"Ошибка при создании аннотации: {e}")
        raise