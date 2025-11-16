import argparse
import csv 
import os
import sys
import time
 
from pathlib import Path

try:
    from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
except ImportError:
    print("Ошибка: Не установлен icrawler. Установите: pip install icrawler")
    sys.exit(1)


class ImageDatasetIterator:
    """Итератор по путям к файлам изображений"""
    
    def __init__(self, annotation_file=None, folder_path=None):
        if annotation_file:
            self.paths = self._load_from_annotation(annotation_file)
        elif folder_path:
            self.paths = self._load_from_folder(folder_path)
        else:
            raise ValueError("Необходимо указать либо annotation_file, либо folder_path")
        
        self.index = 0
    
    def _load_from_annotation(self, annotation_file):
        """Загрузка путей из CSV файла аннотации"""
        paths = []
        
        if not os.path.exists(annotation_file):
            print(f"Файл аннотации {annotation_file} не существует")
            return paths
            
        try:
            with open(annotation_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'absolute_path' in row and os.path.exists(row['absolute_path']):
                        paths.append(row['absolute_path'])
            print(f"Загружено {len(paths)} путей из аннотации")
        except Exception as e:
            print(f"Ошибка при загрузке аннотации: {e}")
        return paths
    
    def _load_from_folder(self, folder_path):
        """Загрузка путей из папки"""
        paths = []
        
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует")
            return paths
            
        try:
            folder = Path(folder_path)
            # Ищем все файлы с изображениями
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp']:
                paths.extend([str(p) for p in folder.rglob(ext)])
                paths.extend([str(p) for p in folder.rglob(ext.upper())])
            
            # Убираем дубликаты
            paths = list(set(paths))
            print(f"Найдено {len(paths)} изображений в папке")
        except Exception as e:
            print(f"Ошибка при загрузке из папки: {e}")
        
        return paths
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.paths)


def download_images_simple(keywords, num_images_per_keyword, output_dir):
    """
    Упрощенная версия скачивания изображений
    """
    print(f"Скачивание {len(keywords) * num_images_per_keyword} изображений...")
    print(f"Ключевые слова: {', '.join(keywords)}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_downloaded_files = []
    
    for keyword in keywords:
        print(f"\n--- Скачивание для: '{keyword}' ---")
        
        # Создаем папку для ключевого слова
        keyword_dir = output_path / keyword.replace(' ', '_')
        keyword_dir.mkdir(exist_ok=True)
        
        try:
            # Используем GoogleImageCrawler
            crawler = GoogleImageCrawler(
                storage={'root_dir': str(keyword_dir)},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2,
            )
            
            print(f"Запуск скачивания...")
            crawler.crawl(
                keyword=keyword,
                max_num=num_images_per_keyword
            )
            
            # Ждем завершения
            print("Ожидание завершения...")
            time.sleep(10)
            
            # Проверяем скачанные файлы
            downloaded_files = []
            for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                downloaded_files.extend(keyword_dir.glob(f'*{ext}'))
                downloaded_files.extend(keyword_dir.glob(f'*{ext.upper()}'))
            
            print(f"Найдено файлов: {len(downloaded_files)}")
            all_downloaded_files.extend(downloaded_files)
            
        except Exception as e:
            print(f" Ошибка при скачивании '{keyword}': {e}")
            print("Пробуем продолжить со следующим ключевым словом...")
            continue
    
    return all_downloaded_files


def create_annotation_csv(image_files, output_dir, annotation_file):
    """
    Создание CSV файла аннотации
    """
    print(f"\nСоздание аннотации: {annotation_file}")
    
    # Создаем папку для аннотации
    annotation_path = Path(annotation_file)
    annotation_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute_path', 'relative_path'])
        
        output_path = Path(output_dir)
        valid_count = 0
        
        for image_file in image_files:
            img_path = Path(image_file)
            
            if not img_path.exists():
                continue
                
            abs_path = str(img_path.absolute())
            
            # Относительный путь
            try:
                rel_path = str(img_path.relative_to(output_path))
            except ValueError:
                rel_path = str(img_path.name)
            
            writer.writerow([abs_path, rel_path])
            valid_count += 1
    
    print(f"Аннотация создана. Записано {valid_count} строк.")


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='Скачивание изображений и создание аннотации'
    )
    
    parser.add_argument('--output_dir', '-o', required=True, 
                       help='Путь к папке для сохранения изображений')
    parser.add_argument('--annotation_file', '-a', required=True,
                       help='Путь к файлу аннотации (CSV)')
    parser.add_argument('--keywords', '-k', nargs='+', required=True,
                       help='Ключевые слова для поиска изображений')
    parser.add_argument('--num_per_keyword', '-n', type=int, required=True,
                       help='Количество изображений для каждого ключевого слова')
    
  
    args = parser.parse_args()
    
    
    
    # Проверяем аргументы
    if args.num_per_keyword <= 0:
        print("Ошибка: количество изображений должно быть положительным числом")
        sys.exit(1)
    
    if len(args.keywords) == 0:
        print("Ошибка: необходимо указать хотя бы одно ключевое слово")
        sys.exit(1)
    
    total_images = len(args.keywords) * args.num_per_keyword
    print(f"Всего будет скачано: {total_images} изображений")
    
    if total_images < 50:
        print(f"  Предупреждение: количество изображений ({total_images}) меньше 50")
        response = input("Продолжить? (y/n): ").lower()
        if response != 'y':
            print("Отмена выполнения")
            sys.exit(0)
    
    # Скачиваем изображения
    downloaded_files = download_images_simple(
        args.keywords, 
        args.num_per_keyword, 
        args.output_dir
    )
    
    if not downloaded_files:
        print(" Не удалось скачать ни одного изображения")
        print("Возможные причины:")
        print("1. Проблемы с интернет-соединением")
        print("2. Антивирус блокирует скачивание") 
        print("3. Ключевые слова не найдены")
        print("4. Проблемы с библиотекой icrawler")
        sys.exit(1)
    
    # Создаем аннотацию
    create_annotation_csv(downloaded_files, args.output_dir, args.annotation_file)
    
    print(f"\n Успешно завершено!")
    print(f" Изображения: {args.output_dir}")
    print(f" Аннотация: {args.annotation_file}")
    print(f"  Скачано: {len(downloaded_files)} изображений")


if __name__ == "__main__":
    main()