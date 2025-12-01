import os
import csv
import argparse
import random
import time
from pathlib import Path
from typing import List, Tuple, Dict
from icrawler.builtin import BingImageCrawler


class ImageIterator:
    """Итератор для путей изображений из CSV аннотации."""
    
    def __init__(self, annotation_file: str) -> None:
        self.annotation_file = annotation_file
        self.data = []
        self.index = 0
        self._load_data()
    
    def _load_data(self) -> None:
        """Загрузка данных из CSV файла."""
        if os.path.exists(self.annotation_file):
            with open(self.annotation_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                self.data = [row for row in reader]
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Dict[str, str]:
        """Возвращает следующий путь к файлу."""
        if self.index < len(self.data):
            row = self.data[self.index]
            self.index += 1
            return {'absolute': row[0], 'relative': row[1]}
        raise StopIteration


def cleanup_temp_files(directory: str) -> None:
    """Удаление временных файлов в директории."""
    for file_path in Path(directory).rglob('*.*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.tmp']:
            try:
                file_path.unlink()
            except:
                pass


def download_fish_images(
    output_dir: str,
    size_ranges: List[Tuple[int, int]],
    min_total: int = 80,
    max_total: int = 200
) -> List[Tuple[str, str]]:
    """Скачивание изображений рыб с разными размерами."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Случайное распределение по диапазонам
    total = random.randint(min_total, max_total)
    num_ranges = len(size_ranges)
    counts = []
    remaining = total
    
    for i in range(num_ranges):
        if i == num_ranges - 1:
            count = remaining
        else:
            min_count = max(20, remaining // (num_ranges - i) // 2)
            count = random.randint(min_count, remaining - (num_ranges - i - 1) * 20)
            remaining -= count
        counts.append(count)
    
    print(f"Скачивание {sum(counts)} изображений")
    all_files = []
    
    # Скачивание для каждого диапазона
    for i, (min_size, max_size) in enumerate(size_ranges):
        range_dir = os.path.join(output_dir, f"range_{i+1}")
        os.makedirs(range_dir, exist_ok=True)
        cleanup_temp_files(range_dir)
        
        downloaded = 0
        keywords = ['fish', 'aquarium fish', 'tropical fish']
        
        for attempt in range(2):
            try:
                crawler = BingImageCrawler(storage={'root_dir': range_dir})
                keyword = random.choice(keywords)
                target = counts[i] * 2 if attempt == 0 else counts[i] - downloaded
                
                crawler.crawl(keyword=keyword, max_num=target, file_idx_offset='auto')
                time.sleep(2)
                
            except Exception as e:
                print(f"Ошибка: {e}")
                continue
            
            # Сбор скачанных файлов
            current_files = []
            for file_path in Path(range_dir).rglob('*.*'):
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    if file_path.stat().st_size > 10240:
                        abs_path = str(file_path.absolute())
                        rel_path = str(file_path.relative_to(output_dir))
                        if (abs_path, rel_path) not in all_files + current_files:
                            current_files.append((abs_path, rel_path))
            
            downloaded += len(current_files)
            all_files.extend(current_files)
            
            if downloaded >= counts[i]:
                break
        
        print(f"Диапазон {i+1}: {downloaded}/{counts[i]} изображений")
    
    return all_files


def create_csv_annotation(files: List[Tuple[str, str]], filename: str) -> None:
    """Создание CSV файла с путями к изображениям."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(files)
    print(f"Аннотация сохранена: {filename} ({len(files)} файлов)")


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description='Скачивание изображений рыб')
    parser.add_argument('--output_dir', default='fish_images', help='Папка для сохранения')
    parser.add_argument('--annotation_file', default='annotation.csv', help='Файл аннотации')
    parser.add_argument('--size_ranges', default='300x300,500x500,700x700', help='Диапазоны размеров')
    parser.add_argument('--min_images', type=int, default=80, help='Минимум изображений')
    parser.add_argument('--max_images', type=int, default=200, help='Максимум изображений')
    
    args = parser.parse_args()
    
    # Парсинг диапазонов размеров
    try:
        size_ranges = []
        for r in args.size_ranges.split(','):
            w, h = map(int, r.split('x'))
            size_ranges.append((w, h))
    except:
        print("Ошибка формата диапазонов. Использую стандартные.")
        size_ranges = [(300, 300), (500, 500), (700, 700)]
    
    # Скачивание изображений
    files = download_fish_images(
        args.output_dir, 
        size_ranges, 
        args.min_images, 
        args.max_images
    )
    
    if files:
        create_csv_annotation(files, args.annotation_file)
        
        # Демонстрация итератора
        print("\nПример работы итератора:")
        for i, file_info in enumerate(ImageIterator(args.annotation_file)):
            if i < 3:
                print(f"  {file_info['relative']}")
            else:
                break
    else:
        print("Не скачано ни одного изображения")


if __name__ == "__main__":
    main()