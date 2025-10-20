import argparse
import csv
import os
import time
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


"""Подготовка папки для скачивания изображений"""
def download_bear_images(date_ranges, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Скачивание изображений медведей...")
    print(f"Количество диапазонов дат: {len(date_ranges)}")
    print(f"Цель: 50-1000 изображений")
    
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
    
    total_downloaded = 0
    max_attempts_per_range = 3 


    """Скачивание изображений для каждого диапазона дат"""
    for range_idx, (start_date, end_date) in enumerate(date_ranges):
        print(f"\n=== Диапазон {range_idx + 1}: {start_date} - {end_date} ===")
        
        range_dir = os.path.join(output_dir, f"range_{range_idx + 1}")
        os.makedirs(range_dir, exist_ok=True)
        
        for attempt in range(max_attempts_per_range):
            if total_downloaded >= 1000:  
                break
                
            keyword = bear_keywords[attempt % len(bear_keywords)]
            
            if total_downloaded < 50:
                to_download = 100
            elif total_downloaded < 500:
                to_download = 200
            else:
                to_download = min(1000 - total_download, 200)
            
            search_query = f"{keyword} after:{start_date} before:{end_date}"
            
            print(f"  Попытка {attempt + 1}: '{keyword}'")
            print(f"  Скачиваем: {to_download} изображений")
            
            try:
                crawler = BingImageCrawler(
                    storage={'root_dir': range_dir},
                    downloader_threads=2
                )
                
                crawler.crawl(keyword=search_query, max_num=to_download)
                
                """Считаю общее количество файлов во всех диапазонах"""
                current_files = []
                for file_path in Path(output_dir).rglob('*'):
                    if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        current_files.append(str(file_path.resolve()))
                
                total_downloaded = len(current_files)
                print(f"  Всего скачано: {total_downloaded}")
                
                if total_downloaded >= 50 and attempt >= 1 and total_downloaded >= 300:
                    break
                
                time.sleep(3)
                
            except Exception as e:
                print(f"  Ошибка: {e}")
                time.sleep(5)
        
        
        if total_downloaded >= 1000:
            break
    
    """Собираю все файлы из всех диапазонов"""
    final_files = []
    for file_path in Path(output_dir).rglob('*'):
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            final_files.append(str(file_path.resolve()))
    
    
    if len(final_files) > 1000:
        files_to_delete = final_files[1000:]
        for path in files_to_delete:
            try:
                os.remove(path)
            except:
                pass
        final_files = final_files[:1000]
        print(f"Удалено лишних: {len(files_to_delete)}")
    
    return final_files


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
        description='Скачивание 50-1000 изображений медведей по диапазонам дат'
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
        help='Диапазоны дат через запятую: start1-end1,start2-end2 (например: 2023-01-01-2023-03-31,2023-04-01-2023-06-30,2023-07-01-2023-09-30)'
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