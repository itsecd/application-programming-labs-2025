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


"""Разбор строки диапазона на начальную и конечную даты"""
def parse_single_date_range(date_arg):
    parts = date_arg.split('-')
    if len(parts) != 6:
        raise ValueError("Неверный формат даты. Используйте: ГГГГ-ММ-ДД-ГГГГ-ММ-ДД")
    
    start_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
    end_date = f"{parts[3]}-{parts[4]}-{parts[5]}"
    
    return start_date, end_date


"""Подготовка папки для скачивания изображений(Очищает папку от старых файлов перед новым скачиванием, чтобы не смешивать результаты)"""
def download_bear_images(start_date, end_date, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Скачивание изображений медведей...")
    print(f"Диапазон дат: {start_date} - {end_date}")
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
    max_attempts = 10  


    """Этот блок скачивает изображения с контролем количества (50-1000 штук)"""
    for attempt in range(max_attempts):
        if total_downloaded >= 1000:  
            break
            
        keyword = bear_keywords[attempt % len(bear_keywords)]
        
        if total_downloaded < 50:
            to_download = 100  
        elif total_downloaded < 500:
            to_download = 200  
        else:
            to_download = 1000 - total_download  
        
        search_query = f"{keyword} after:{start_date} before:{end_date}"
        
        print(f"\nПопытка {attempt + 1}: '{keyword}'")
        print(f"Скачиваем: {to_download} изображений")
        
        try:
            crawler = BingImageCrawler(
                storage={'root_dir': output_dir},
                downloader_threads=2
            )
            
            crawler.crawl(keyword=search_query, max_num=to_download)
            
            current_files = []
            for file_path in Path(output_dir).rglob('*'):
                if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    current_files.append(str(file_path.resolve()))
            
            total_downloaded = len(current_files)
            print(f"Всего скачано: {total_downloaded}")
            
            if total_downloaded >= 50:
                print(f"Достигнут минимум 50 изображений")
                if attempt >= 5 and total_downloaded >= 500:  
                    break
            
            time.sleep(3)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)
    
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


"""Создает (csv)файл аннотации, где для каждого изображения хранится его полный путь и путь относительно папки с изображениями"""
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
    parser = argparse.ArgumentParser(description='Скачивание 50-1000 изображений медведей по диапазону дат')
    parser.add_argument('--output_dir', required=True,help='Папка для сохранения изображений')
    parser.add_argument('--annotation_file', required=True, help='CSV файл аннотации')
    parser.add_argument('--date_range', required=True, help='Диапазон дат: start-end (например: 2023-01-01-2023-12-31)')
    
    args = parser.parse_args()
    
    try:
        start_date, end_date = parse_single_date_range(args.date_range)
        print(f"Диапазон дат: {start_date} - {end_date}")
    except ValueError as e:
        print(f"Ошибка в формате даты: {e}")
        return
    
    image_paths = download_bear_images(start_date, end_date, args.output_dir)
    
    print(f"\nРЕЗУЛЬТАТ: Скачано {len(image_paths)} изображений")
    
    if len(image_paths) < 50:
        print("ВНИМАНИЕ: Не удалось достичь минимума в 50 изображений")
        print("Возможные причины:")
        print("1. Ограничения поисковика")
        print("2. Мало результатов по данному диапазону дат")
        print("3. Попробуйте другой диапазон дат")
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