import argparse
import csv
import os
from typing import Iterator, List, Dict
from icrawler.builtin import GoogleImageCrawler


class ImagePathIterator:    
    def __init__(self, annotation_file: str) -> None:

        self.annotation_file = annotation_file
        if not os.path.exists(annotation_file):
            raise FileNotFoundError(f"Файл аннотации {annotation_file} не найден")
        
        self._load_paths()
    
    def _load_paths(self) -> None:
        self.paths: List[Dict[str, str]] = []
        try:
            with open(self.annotation_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.paths.append(row)
        except Exception as e:
            raise IOError(f"Ошибка чтения файла аннотации: {e}")
    
    def __iter__(self) -> Iterator[Dict[str, str]]:
        self.current_index = 0
        return self
    
    def __next__(self) -> Dict[str, str]:

        if self.current_index < len(self.paths):
            result = self.paths[self.current_index]
            self.current_index += 1
            return result
        else:
            raise StopIteration


def download_images(keyword: str, min_size: str, max_size: str, 
                   output_dir: str, max_num: int = 100) -> None:

    try:
        os.makedirs(output_dir, exist_ok=True)
        
        filters = dict(
            size=(min_size, max_size)
        )
        
        crawler = GoogleImageCrawler(
            storage={'root_dir': output_dir},
            feeder_threads=2,
            parser_threads=4,
            downloader_threads=8
        )
        
        crawler.crawl(
            keyword=keyword,
            filters=filters,
            max_num=max_num,
            file_idx_offset=0
        )
        
        print(f"Скачано изображений в папку: {output_dir}")
        
    except Exception as e:
        raise Exception(f"Ошибка при скачивании изображений: {e}")


def create_annotation(output_dir: str, annotation_file: str) -> None:

    try:
        image_files = []
        for filename in os.listdir(output_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                abs_path = os.path.abspath(os.path.join(output_dir, filename))
                rel_path = os.path.relpath(abs_path)
                image_files.append({
                    'absolute_path': abs_path,
                    'relative_path': rel_path,
                    'filename': filename
                })
        
        with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['absolute_path', 'relative_path', 'filename']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for image in image_files:
                writer.writerow(image)
        
        print(f"Создана аннотация: {annotation_file}")
        print(f"Записано записей: {len(image_files)}")
        
    except IOError as e:
        raise IOError(f"Ошибка при создании аннотации: {e}")


def main() -> None:

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        'output_dir', 
        type=str
    )
    parser.add_argument(
        'annotation_file', 
        type=str
    )
    
    parser.add_argument(
        '--keyword', 
        type=str, 
        default='cat'
    )
    parser.add_argument(
        '--min-size', 
        type=str, 
        default='200x200'
    )
    parser.add_argument(
        '--max-size', 
        type=str, 
        default='1000x1000'
  
    )
    parser.add_argument(
        '--max-num', 
        type=int, 
        default=100
    )
    
    args = parser.parse_args()
    
    try:
     
        print(f"Начинаем скачивание изображений по ключевому слову: '{args.keyword}'")
        download_images(
            keyword=args.keyword,
            min_size=args.min_size,
            max_size=args.max_size,
            output_dir=args.output_dir,
            max_num=args.max_num
        )
        
        create_annotation(args.output_dir, args.annotation_file)
        
      
        print("\nДемонстрация работы итератора:")
        iterator = ImagePathIterator(args.annotation_file)
        
        count = 0
        max_display = 5 
        
        for path_info in iterator:
            if count < max_display:
                print(f"Абсолютный путь: {path_info['absolute_path']}")
                print(f"Относительный путь: {path_info['relative_path']}")
                print(f"Имя файла: {path_info['filename']}")
                print("-" * 50)
            count += 1
        
        print(f"Всего записей в аннотации: {count}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
