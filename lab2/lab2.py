import argparse
import csv
import os
import time
from icrawler.builtin import BingImageCrawler


class ImageIterator:
    def __init__(self, annotation_file=None, folder_path=None):
        self.paths = []
        
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

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


def main():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description='Скачать изображения свиней')
    parser.add_argument('--output-dir', required=True, help='Папка для изображений')
    parser.add_argument('--annotation-file', required=True, help='Файл для аннотации')
    parser.add_argument('--timeout', type=int, required=True, help='Время в секундах')
    
    args = parser.parse_args()

    # Создаем папку если нет
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Скачиваем изображения 'pig'...")
    print(f"Время: {args.timeout} сек")
    print(f"Папка: {args.output_dir}")

    # Засекаем время
    start_time = time.time()

    # Скачиваем изображения
    crawler = BingImageCrawler(storage={'root_dir': args.output_dir})
    crawler.crawl(keyword='pig', max_num=50)

    # Считаем время
    elapsed_time = time.time() - start_time

    # Создаем CSV аннотацию
    with open(args.annotation_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Абсолютный путь', 'Относительный путь'])
        
        # Записываем пути ко всем изображениям
        for file in os.listdir(args.output_dir):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                abs_path = os.path.abspath(os.path.join(args.output_dir, file))
                rel_path = os.path.join(args.output_dir, file)
                writer.writerow([abs_path, rel_path])

    # Считаем сколько скачали
    image_count = len([f for f in os.listdir(args.output_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])

    # Выводим результаты
    print(f"\nГотово!")
    print(f"Скачано: {image_count} изображений")
    print(f"Время: {elapsed_time:.1f} сек")
    print(f"Аннотация: {args.annotation_file}")

    #работа итератора
    print(f"\nИтератор из аннотации:")
    iterator = ImageIterator(annotation_file=args.annotation_file)
    for i, path in enumerate(iterator):
        if i < 3:  # Показываем первые 3 пути
            print(f"  {path}")
    print(f"Всего путей: {i + 1}")


if __name__ == "__main__":
    main()