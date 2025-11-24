import os
import csv
import argparse
import random
import time
from icrawler.builtin import BingImageCrawler
from pathlib import Path

class ImageIterator:
    def __init__(self, annotation_file):
        self.annotation_file = annotation_file
        self.data = []
        self.load_annotation()
        self.index = 0
    
    def load_annotation(self):
        if os.path.exists(self.annotation_file):
            with open(self.annotation_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                self.data = [row for row in reader]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            row = self.data[self.index]
            self.index += 1
            return {
                'absolute_path': row[0],
                'relative_path': row[1]
            }
        else:
            raise StopIteration

def cleanup_directory(directory):
    for file_path in Path(directory).rglob('*.*'):
        if file_path.is_file():
            if file_path.suffix.lower() in ['.txt', '.tmp', '']:
                try:
                    file_path.unlink()
                except:
                    pass

def download_images(output_dir, size_ranges, total_min=80, total_max=200):
    os.makedirs(output_dir, exist_ok=True)
    
    num_ranges = len(size_ranges)
    remaining = random.randint(total_min, total_max)
    counts = []
    
    for i in range(num_ranges):
        if i == num_ranges - 1:
            count = remaining
        else:
            min_count = max(20, remaining // (num_ranges - i) // 2)
            max_count = remaining - (num_ranges - i - 1) * 20
            count = random.randint(min_count, max_count)
            remaining -= count
        counts.append(count)
    
    print(f"Будет скачано изображений по диапазонам: {dict(zip(size_ranges, counts))}")
    print(f"Общее количество: {sum(counts)}")
    
    all_files = []
    
    for i, (min_size, max_size) in enumerate(size_ranges):
        range_dir = os.path.join(output_dir, f"range_{i+1}")
        os.makedirs(range_dir, exist_ok=True)
        
        count = counts[i]
        print(f"\n=== Диапазон {i+1}: {min_size}x{max_size} ===")
        print(f"Цель: {count} изображений")
        
        cleanup_directory(range_dir)
        
        downloaded_count = 0
        keywords = ['fish', 'fishes', 'aquarium fish', 'colorful fish', 'tropical fish', 'marine fish']
        
        for attempt in range(2):
            try:
                crawler = BingImageCrawler(
                    storage={'root_dir': range_dir},
                    feeder_threads=3,
                    parser_threads=3,
                    downloader_threads=6
                )
                
                keyword = random.choice(keywords)
                target_count = count * 2 if attempt == 0 else count - downloaded_count
                
                print(f"Попытка {attempt + 1}: поиск '{keyword}' ({target_count} изображений)")
                
                crawler.crawl(
                    keyword=keyword,
                    max_num=target_count,
                    file_idx_offset='auto'
                )
                
                time.sleep(3)
                
            except Exception as e:
                print(f"Ошибка при скачивании: {e}")
                continue
            
            cleanup_directory(range_dir)
            
            current_files = []
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
            
            for file_path in Path(range_dir).rglob('*.*'):
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    if file_path.stat().st_size > 10240:
                        absolute_path = str(file_path.absolute())
                        relative_path = str(file_path.relative_to(output_dir))
                        if (absolute_path, relative_path) not in all_files + current_files:
                            current_files.append((absolute_path, relative_path))
            
            downloaded_count += len(current_files)
            all_files.extend(current_files)
            print(f"Скачано в попытке {attempt + 1}: {len(current_files)} изображений")
            
            if downloaded_count >= count:
                break
        
        print(f"Итого для диапазона {i+1}: {downloaded_count} изображений")
    
    return all_files

def create_annotation(files, annotation_file):
    with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(files)
    
    print(f"Аннотация создана: {annotation_file}")
    print(f"Всего файлов в аннотации: {len(files)}")

def main():
    parser = argparse.ArgumentParser(description='Скачивание изображений fish с разными диапазонами размеров')
    parser.add_argument('--output_dir', type=str, default='fish_images')
    parser.add_argument('--annotation_file', type=str, default='fish_annotation.csv')
    parser.add_argument('--size_ranges', type=str, default='300x300,500x500,700x700,900x900')
    parser.add_argument('--min_images', type=int, default=80)
    parser.add_argument('--max_images', type=int, default=200)
    
    args = parser.parse_args()
    
    size_ranges = []
    for range_str in args.size_ranges.split(','):
        try:
            min_size, max_size = map(int, range_str.split('x'))
            size_ranges.append((min_size, max_size))
        except ValueError:
            print(f"Некорректный формат диапазона: {range_str}")
            return
    
    print(f"Диапазоны размеров: {size_ranges}")
    print(f"Целевое количество изображений: {args.min_images}-{args.max_images}")
    
    downloaded_files = download_images(args.output_dir, size_ranges, args.min_images, args.max_images)
    
    if not downloaded_files:
        print("Не удалось скачать ни одного изображения!")
        return
    
    create_annotation(downloaded_files, args.annotation_file)
    
    print("\nДемонстрация работы итератора:")
    iterator = ImageIterator(args.annotation_file)
    file_count = 0
    for file_info in iterator:
        if file_count < 5:
            print(f"Файл {file_count+1}: {file_info['relative_path']}")
            file_count += 1
        else:
            break

if __name__ == "__main__":
    main()