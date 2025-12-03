import argparse
import csv
import random
from datetime import datetime
from pathlib import Path
from typing import Iterator, Tuple
from icrawler.builtin import BingImageCrawler


def get_date_ranges_from_user(num_ranges: int) -> list[tuple[str, str]]:
    """
    Пользователь вводит диапазоны дат вручную.
    """
    date_ranges = []
    print("Введите диапазоны дат в формате ГГГГ-ММ-ДД:")
    
    for i in range(num_ranges):
        print(f"\nДиапазон {i+1}:")
        start_date = input("  Начальная дата: ").strip()
        end_date = input("  Конечная дата: ").strip()
        date_ranges.append((start_date, end_date))
    
    return date_ranges


def download_bear_images(output_dir: str, date_ranges: list[tuple[str, str]], total_images: int) -> None:
    """
    Скачивает изображения медведей по заданным диапазонам дат.
    Гарантирует скачивание от 50 до 1000 изображений.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Проверяем ограничение 50-1000
    if total_images < 50 or total_images > 1000:
        print("Ошибка: количество изображений должно быть от 50 до 1000!")
        return
    
    # Распределяем общее количество по диапазонам (каждому не менее 1)
    num_ranges = len(date_ranges)
    images_per_range = [1] * num_ranges  # Каждому диапазону минимум 1
    
    # Распределяем оставшиеся изображения случайным образом
    remaining = total_images - num_ranges
    for _ in range(remaining):
        images_per_range[random.randint(0, num_ranges - 1)] += 1
    
    print(f"Общее количество изображений: {total_images}")
    print(f"Распределение по диапазонам: {images_per_range}")
    
    total_downloaded = 0
    
    # Скачиваем для каждого диапазона
    for i, (start_date, end_date) in enumerate(date_ranges):
        target = images_per_range[i]
        
        print(f"\nДиапазон {i+1}: {start_date} - {end_date}")
        print(f"Цель: {target} изображений")
        
        try:
            crawler = BingImageCrawler(storage={'root_dir': output_dir})
            crawler.crawl(
                keyword=f"bear after:{start_date} before:{end_date}",
                max_num=target
            )
        except Exception as e:
            print(f"Ошибка: {e}")
            continue
        
        # Подсчитываем скачанные файлы
        current_files = list(Path(output_dir).glob("*.jpg"))
        current_count = len(current_files)
        downloaded_in_range = current_count - total_downloaded
        total_downloaded = current_count
        
        print(f"Скачано в этом диапазоне: {downloaded_in_range}")
        print(f"Общий прогресс: {total_downloaded}/{total_images}")
    
    # Гарантируем минимум 50 изображений
    if total_downloaded < 50:
        need = 50 - total_downloaded
        print(f"\nНедостаточно изображений! Докачиваем ещё {need}...")
        
        try:
            crawler = BingImageCrawler(storage={'root_dir': output_dir})
            crawler.crawl(keyword="bear", max_num=need)
        except Exception as e:
            print(f"Ошибка доп. загрузки: {e}")
    
    final_count = len(list(Path(output_dir).glob("*.jpg")))
    print(f"\nИтого скачано: {final_count} изображений")
    
    # Проверяем итоговое количество
    if final_count < 50:
        print("ВНИМАНИЕ: Не удалось скачать минимальное количество 50 изображений!")
    elif final_count > 1000:
        print("ВНИМАНИЕ: Скачано больше 1000 изображений!")


def create_annotation(images_dir: str, annotation_file: str) -> None:
    """
    Создает CSV-аннотацию с путями к файлам.
    """
    with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Абсолютный путь', 'Относительный путь'])
        
        for img_path in Path(images_dir).glob("*.jpg"):
            absolute_path = img_path.absolute()
            relative_path = img_path.relative_to(Path(images_dir).parent)
            writer.writerow([str(absolute_path), str(relative_path)])
    
    print(f"Аннотация создана: {annotation_file}")


class FilePathIterator:
    """Итератор для перебора
путей к файлам из аннотации."""
    
    def __init__(self, annotation_file: str) -> None:
        self.annotation_file = annotation_file
        self.lines = []
        self.index = 0
        
        try:
            with open(annotation_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.lines = list(reader)[1:]
        except FileNotFoundError:
            pass
    
    def __iter__(self) -> 'FilePathIterator':
        self.index = 0
        return self
    
    def __next__(self) -> Tuple[str, str]:
        if self.index < len(self.lines):
            row = self.lines[self.index]
            self.index += 1
            if len(row) >= 2:
                return row[0], row[1]
        raise StopIteration


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description='Скачивание изображений медведей')
    parser.add_argument('--output_dir', type=str, default='bear_images',
                       help='Папка для изображений')
    parser.add_argument('--annotation_file', type=str, default='annotation.csv',
                       help='Файл аннотации')
    parser.add_argument('--num_ranges', type=int, default=3,
                       help='Количество диапазонов дат')
    parser.add_argument('--total_images', type=int, default=50,
                       help='Общее количество изображений (от 50 до 1000)')
    
    args = parser.parse_args()
    
    # Проверяем количество изображений
    if args.total_images < 50 or args.total_images > 1000:
        print("Ошибка: количество изображений должно быть от 50 до 1000!")
        return
    
    # 1. Пользователь задает диапазоны дат
    print("=== Ввод диапазонов дат ===")
    date_ranges = get_date_ranges_from_user(args.num_ranges)
    
    # 2. Скачиваем изображения
    print("\n=== Скачивание изображений ===")
    download_bear_images(args.output_dir, date_ranges, args.total_images)
    
    # 3. Создаем аннотацию
    print("\n=== Создание аннотации ===")
    create_annotation(args.output_dir, args.annotation_file)
    
    # 4. Демонстрируем итератор
    print("\n=== Демонстрация итератора ===")
    iterator = FilePathIterator(args.annotation_file)
    
    file_count = 0
    for absolute, relative in iterator:
        if file_count < 3:
            print(f"Абсолютный: {absolute}")
            print(f"Относительный: {relative}")
            print("---")
        file_count += 1
    
    print(f"Всего файлов в аннотации: {file_count}")


if __name__ == '__main__':
    main()
