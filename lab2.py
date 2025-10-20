import argparse
import csv
import os
import time
import random
from pathlib import Path
from icrawler.builtin import BingImageCrawler
from PIL import Image


"""Поиск пути к картинкам"""
class ImageIterator:
    def __init__(self, source):
        self.paths = []
        self.counter = 0
        
        if os.path.isfile(source) and source.endswith('.csv'):
            with open(source, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.paths.append(row['absolute_path'])
        elif os.path.isdir(source):
            image_extensions = ['.jpg', '.jpeg', '.png']
            for file_path in Path(source).rglob('*'):
                if file_path.suffix.lower() in image_extensions:
                    self.paths.append(str(file_path))
        else:
            raise ValueError("Источник должен быть CSV файлом или папкой")
        

    """Класс становится итерируемым для его дальнейшего использования"""
    def __iter__(self):
        self.counter = 0
        return self
    

    """Выдает следующий путь к картинке из списка, пока пути не кончатся"""
    def __next__(self):
        if self.counter < len(self.paths):
            path = self.paths[self.counter]
            self.counter += 1
            return path
        else:
            raise StopIteration


"""Разбор строки диапазонов на начальные и конечные даты"""
def parse_date_ranges(date_args):
    ranges = []
    range_strings = date_args.split(',')
    
    for range_str in range_strings:
        parts = range_str.split('-')
        if len(parts) != 6:
            raise ValueError(f"Неверный формат даты в диапазоне '{range_str}'. Используйте: ГГГГ-ММ-ДД-ГГГГ-ММ-ДД")
        
        start_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        end_date = f"{parts[3]}-{parts[4]}-{parts[5]}"
        ranges.append((start_date, end_date))
    
    return ranges


"""Распределение случайного количества изображений по диапазонам"""
def distribute_images_randomly(date_ranges):
    total_images = random.randint(50, 1000)
    num_ranges = len(date_ranges)
    
    
    images_per_range = [1] * num_ranges
    
    """Распределяем оставшиеся изображения случайным образом"""
    remaining_images = total_images - num_ranges
    
    for _ in range(remaining_images):
        range_index = random.randint(0, num_ranges - 1)
        images_per_range[range_index] += 1
    
    return total_images, images_per_range


"""Скачивание изображений для каждого диапазона дат"""
def download_bear_images(date_ranges, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    """"Распределяем случайное количество изображений по диапазонам"""
    total_images, images_per_range = distribute_images_randomly(date_ranges)
    
    print(f"Скачивание изображений медведей...")
    print(f"Количество диапазонов дат: {len(date_ranges)}")
    print(f"Общее количество изображений: {total_images}")
    print(f"Распределение по диапазонам: {images_per_range}")
    
    if os.path.exists(output_dir):
        for file in Path(output_dir).rglob('*'):
            try:
                file.unlink()
            except:
                pass
    
    """Запросы для поиска медведей"""
    bear_keywords = [
        "brown bear ursus arctos wildlife",
        "grizzly bear animal nature", 
        "eurasian brown bear forest",
        "bear mammal wildlife park",
        "ursus bear species animal"
    ]
    
    all_downloaded_paths = []
    
    """Скачивание для каждого диапазона дат"""
    for range_idx, (start_date, end_date) in enumerate(date_ranges):
        images_for_this_range = images_per_range[range_idx]
        
        print(f"\n=== Диапазон {range_idx + 1}: {start_date} - {end_date} ===")
        print(f"Цель: {images_for_this_range} изображений")
        
        range_dir = os.path.join(output_dir, f"range_{range_idx + 1}")
        os.makedirs(range_dir, exist_ok=True)
        
        keyword = bear_keywords[range_idx % len(bear_keywords)]
        search_query = f"{keyword} after:{start_date} before:{end_date}"
        
        print(f"Поисковый запрос: '{keyword}'")
        
        try:
            crawler = BingImageCrawler(
                storage={'root_dir': range_dir},
                downloader_threads=2
            )
            
            crawler.crawl(keyword=search_query, max_num=images_for_this_range + 10)
            
            time.sleep(2)
            
            range_files = []
            for file_path in Path(range_dir).rglob('*'):
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    range_files.append(str(file_path.resolve()))
            
            actual_downloaded = len(range_files)
            print(f"Скачано для диапазона {range_idx + 1}: {actual_downloaded} изображений")
            
            all_downloaded_paths.extend(range_files)
            
        except Exception as e:
            print(f"Ошибка при скачивании для диапазона {range_idx + 1}: {e}")
    
    """Если общее количество превысило нужное, обрезаю до нужного количества"""
    if len(all_downloaded_paths) > total_images:
        
        files_to_keep = []
        ranges_used = set()
        
        """Собираю по одному файлу из каждого диапазона пока не наберем нужное количество"""
        while len(files_to_keep) < total_images:
            for range_idx in range(len(date_ranges)):
                if len(files_to_keep) >= total_images:
                    break
                
                range_files = [f for f in all_downloaded_paths if f"range_{range_idx + 1}" in f and f not in files_to_keep]
                if range_files:
                    files_to_keep.append(range_files[0])
        
        """Удаляю лишние файлы"""
        files_to_delete = set(all_downloaded_paths) - set(files_to_keep)
        for path in files_to_delete:
            try:
                os.remove(path)
            except:
                pass
        
        all_downloaded_paths = files_to_keep
        print(f"Удалено лишних файлов: {len(files_to_delete)}")
    
    return all_downloaded_paths


"""Создает CSV файл аннотации"""
def create_annotation_csv(image_paths, annotation_file, output_dir):
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute_path', 'relative_path'])
        
        for abs_path in image_paths:
            rel_path = os.path.relpath(abs_path, output_dir)
            writer.writerow([abs_path, rel_path])
    
    print(f"Аннотация создана: {annotation_file}")
    

"""Обрабатывает аргументы и запускает весь процесс"""
def main():
    parser = argparse.ArgumentParser(
        description='Скачивание 50-1000 изображений медведей по диапазонам дат со случайным распределением'
    )
    parser.add_argument(
        '--output_dir', 
        required=True,
        help='Папка для сохранения изображений'
    )
    parser.add_argument(
        '--annotation_file', 
        required=True, 
        help='CSV файл аннотации'
    )
    parser.add_argument(
        '--date_ranges', 
        required=True,
        help='Диапазоны дат через запятую: start1-end1,start2-end2 (например: 2023-01-01-2023-03-31,2023-04-01-2023-06-30)'
    )
    
    args = parser.parse_args()
    
    try:
        date_ranges = parse_date_ranges(args.date_ranges)
        print(f"Обработано диапазонов дат: {len(date_ranges)}")
        for i, (start, end) in enumerate(date_ranges):
            print(f"  Диапазон {i+1}: {start} - {end}")
    except ValueError as e:
        print(f"Ошибка в формате дат: {e}")
        return
    
    image_paths = download_bear_images(date_ranges, args.output_dir)
    
    print(f"\nРЕЗУЛЬТАТ: Скачано {len(image_paths)} изображений")
    
    if len(image_paths) < 50:
        print("ВНИМАНИЕ: Не удалось достичь минимума в 50 изображений")
        print("Возможные причины:")
        print("1. Ограничения поисковика")
        print("2. Мало результатов по данным диапазонам дат")
        print("3. Попробуйте другие диапазоны дат")
    else:
        print("УСПЕХ: Достигнуто требуемое количество изображений")
    
    create_annotation_csv(image_paths, args.annotation_file, args.output_dir)
    
    print(f"\nДемонстрация итератора:")
    iterator = ImageIterator(args.annotation_file)
    print(f"Всего путей в итераторе: {len(iterator.paths)}")
    
    print("Первые 5 файлов:")
    for i, path in enumerate(iterator):
        if i < 5:
            print(f"  {Path(path).name}")


if __name__ == '__main__':
    main()