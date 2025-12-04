"""
Лабораторная работа №2: Загрузка изображений по ключевому слову.
"""

import argparse
import sys
import csv
from pathlib import Path
from typing import List

from icrawler.builtin import BingImageCrawler


IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}


def download_images(keyword: str, output_dir: Path, max_num: int) -> bool:
    """Загружает изображения из Bing."""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Ошибка создания директории {output_dir}: {e}")
        return False
    
    # Инициализируем crawler для Bing
    try:
        crawler = BingImageCrawler(storage={'root_dir': str(output_dir)})
    except Exception as e:
        print(f"Ошибка инициализации BingImageCrawler: {e}")
        return False
    
    # Пытаемся загрузить изображения
    try:
        crawler.crawl(keyword=keyword, max_num=max_num)
        print(f"Успешная загрузка изображений")
        return True
    except Exception as e:
        print(f"Ошибка при загрузке изображений: {e}")
    return False
    
    
def create_annotation(root_dir: Path, csv_path: Path) -> bool:
    """Создает CSV-аннотацию с путями к файлам."""
    try:
        root_dir = root_dir.resolve()
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        with csv_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Абсолютный путь', 'Относительный путь'])
            
            for file_path in root_dir.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in IMG_EXTENSIONS:
                    abs_path = file_path.resolve()
                    rel_path = abs_path.relative_to(root_dir)
                    writer.writerow([str(abs_path), str(rel_path)])
        return True
    except Exception:
        return False


class ImagePathIterator:
    """Итератор для перебора путей к изображениям."""
    
    def __init__(self, source: str, root_dir: str = None) -> None:
        self._items: List[List[str]] = []
        self._index: int = 0
        self._load_items(source, root_dir)
    
    def __iter__(self) -> 'ImagePathIterator':
        self._index = 0
        return self
    
    def __next__(self) -> List[str]:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item
    
    def _load_items(self, source: str, root_dir: str = None) -> None:
        """Загружает элементы из указанного источника."""
        source_path = Path(source)
        
        if source_path.is_file() and source_path.suffix.lower() == '.csv':
            with source_path.open('r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)
                self._items = [row for row in reader if len(row) >= 2]
        else:
            base_dir = Path(root_dir) if root_dir else source_path
            base_dir = base_dir.resolve()
            for file_path in source_path.rglob('*'):
                if (file_path.is_file() and 
                    file_path.suffix.lower() in IMG_EXTENSIONS):
                    abs_path = file_path.resolve()
                    rel_path = abs_path.relative_to(base_dir)
                    self._items.append([str(abs_path), str(rel_path)])


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description='Загрузка изображений из Bing')
    parser.add_argument('--output-dir', required=True, help='Директория для сохранения изображений')
    parser.add_argument('--annotation-file', required=True, help='Путь к файлу CSV-аннотации')
    parser.add_argument('--images-per-range', type=int, required=True, 
                       help='Количество изображений для каждого диапазона (50-1000)')
    parser.add_argument('--keyword', default='bear', help='Ключевое слово для поиска')
    return parser.parse_args()


def validate_arguments(args) -> bool:
    """Проверяет корректность аргументов командной строки."""
    if not (50 <= args.images_per_range <= 1000):
        print("Ошибка: количество изображений должно быть от 50 до 1000", file=sys.stderr)
        return False
    return True


def main() -> None:
    """Основная функция программы."""
    try:
        args = parse_arguments()
        
        if not validate_arguments(args):
            sys.exit(1)
        
        output_dir = Path(args.output_dir)
        
        # Загрузка изображений
        success = download_images(  
            keyword=args.keyword,
            output_dir=output_dir,
            max_num=args.images_per_range
        )
        
        if not success:
            print(f"Предупреждение: проблемы с загрузкой")
        
        # Создание аннотации
        csv_path = Path(args.annotation_file)
        if not create_annotation(output_dir, csv_path):
            print("Ошибка: не удалось создать аннотацию", file=sys.stderr)
            sys.exit(1)
        
        # Демонстрация работы итератора
        print("Демонстрация работы итератора (первые 5 файлов):")
        iterator = ImagePathIterator(str(csv_path))
        for i, (abs_path, rel_path) in enumerate(iterator):
            if i < 5:
                print(f"  {rel_path}")
        
        for i, (abs_path, rel_path) in enumerate(iterator):
            if i < 5 :
                print(f"  {rel_path}")
        
    except Exception as e:
        print(f"Критическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()