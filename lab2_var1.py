import argparse
import csv
import os
from pathlib import Path

from icrawler.builtin import BingImageCrawler


def create_parser():
    """
    Создание парсера и настройка парсера аргументов командной строки
    """
    parser = argparse.ArgumentParser(
        description='Скачивание изображений и создание аннотации'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        required=True
    )
    parser.add_argument(
        '--annotation_file',
        type=str,
        required=True
    )
    parser.add_argument(
        '--max_num',
        type=int,
        default=100
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10
    )
    parser.add_argument(
        '--size',
        type=str,
        choices=['large', 'medium', 'small', 'wallpaper']
    )
    
    return parser


class ImagePathIterator:
    """
    Класс итератора для перебора путей к файлам изображений
    """
    def __init__(self, source: str):
        self.source = source
        self.file_paths = []
        self.current_index = 0
        
        if os.path.isfile(source) and source.endswith('.csv'):
            self._load_from_annotation(source)
        else:
            raise ValueError("Источник должен быть CSV-файлом")
    
    def _load_from_annotation(self, annotation_file: str):
        """
        загрузка путей из csv файла
        """
        try:
            with open(annotation_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if os.path.exists(row['absolute_path']):
                        self.file_paths.append(row['absolute_path'])
            print(f"Загружено {len(self.file_paths)} путей из аннотации")
        except Exception as e:
            print(f"Ошибка при чтении аннотации: {e}")

    def __iter__(self):
        self.current_index = 0
        return self
    
    def __next__(self):
        if self.current_index < len(self.file_paths):
            path = self.file_paths[self.current_index]
            self.current_index += 1
            return path
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.file_paths)


def download_images(keyword: str, output_dir: str, max_num: int, timeout: int = 10, size: str = None) -> None:
    """
    Скачивание изображений с помощью BingImageCrawler
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"Начинаем скачивание изображений по ключевому слову: '{keyword}'")
    print(f"Максимальное количество: {max_num}")
    filters = {}
    
    try:
        crawler = BingImageCrawler(
            storage={'root_dir': output_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=4,
        )
        
        crawler.downloader.timeout = timeout
        
        crawler.crawl(
            keyword=keyword,
            max_num=max_num,
            file_idx_offset=0,
            filters=filters if filters else None
        )

 
    except Exception as e:
        raise Exception(f"Ошибка при скачивании: {e}")
def count_downloaded_files(output_dir:str)-> int:
    """
    Подсчитываем количество загруженных изображений
    """
    count = 0

    for file_path in Path(output_dir).rglob('*.*'):
            if (file_path.is_file() and 
                file_path.stat().st_size > 0 and
                file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}):
                count += 1
    
    return count

def create_annotation(output_dir: str, annotation_file: str) -> None:
    """
    Создание CSV файла аннотации 
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                absolute_path = os.path.abspath(os.path.join(root, file))
                relative_path = os.path.relpath(absolute_path, start=os.path.dirname(annotation_file))
                image_files.append({
                    'filename': file,
                    'absolute_path': absolute_path,
                    'relative_path': relative_path
                })
    
    if not image_files:
        print("не найдено файлов изображений для аннотации")
    
    with open(annotation_file, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['filename', 'absolute_path', 'relative_path']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for image in image_files:
            writer.writerow(image)
    
    print(f"Аннотация создана: {annotation_file}")
    print(f"Записано {len(image_files)} файлов")


def main():
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        download_images(
            keyword='cat',
            output_dir=args.output_dir,
            max_num=args.max_num,
            timeout=args.timeout,
            size=args.size
        )
        
        create_annotation(args.output_dir, args.annotation_file)
        downloaded_count = count_downloaded_files(args.output_dir)
        iterator = ImagePathIterator(args.annotation_file)

        print(f"Всего файлов для итерации: {len(iterator)}")
        
        count = 0
        for path in iterator:
            print(f"Абсолютный путь: {path}")
            count += 1
            if count >= 5: 
                print("и другие файлы")
                break
        
        if count == 0:
            print("Нет файлов для отображения")
            
    except Exception as e:
        print(f"Ошибка в основной программе: {e}")


if __name__ == "__main__":
    main()
