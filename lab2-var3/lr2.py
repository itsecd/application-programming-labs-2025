import os
import csv
import argparse
import random
import time
from pathlib import Path
from PIL import Image
from icrawler.builtin import BingImageCrawler

class ImageIterator:
    def __init__(self, annotation_file=None, folder=None):
        self.data = []
        if annotation_file:
            self.load_from_csv(annotation_file)
        elif folder:
            self.load_from_folder(folder)
        self.index = 0

    def load_from_csv(self, annotation_file):
        if os.path.exists(annotation_file):
            with open(annotation_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                self.data = [row for row in reader]

    def load_from_folder(self, folder):
        folder = Path(folder)
        for file_path in folder.rglob("*.*"):
            if file_path.is_file():
                self.data.append([str(file_path.absolute()), str(file_path.relative_to(folder))])

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            row = self.data[self.index]
            self.index += 1
            return {'absolute_path': row[0], 'relative_path': row[1]}
        else:
            raise StopIteration

def cleanup_directory(directory):
    if not os.path.exists(directory):
        return
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    for file_path in Path(directory).iterdir():
        if file_path.is_file() and file_path.suffix.lower() not in image_exts:
            try:
                file_path.unlink()
            except:
                pass

def image_matches_size(path, min_size, max_size):
    try:
        with Image.open(path) as img:
            w, h = img.size
            return min_size <= w <= max_size and min_size <= h <= max_size
    except:
        return False

def generate_random_counts(size_ranges, total_min, total_max):
    num_ranges = len(size_ranges)
    remaining = random.randint(total_min, total_max)
    counts = []
    for i in range(num_ranges):
        if i == num_ranges - 1:
            counts.append(remaining)
        else:
            min_count = 1
            max_count = remaining - (num_ranges - i - 1)
            count = random.randint(min_count, max_count)
            remaining -= count
            counts.append(count)
    return counts

def download_images(output_dir, size_ranges, counts):
    os.makedirs(output_dir, exist_ok=True)
    all_files = []
    all_abs = set()
    keywords = ['fish', 'fishes', 'aquarium fish', 'colorful fish', 'tropical fish', 'marine fish']
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    for i, ((min_size, max_size), need_count) in enumerate(zip(size_ranges, counts)):
        range_dir = os.path.join(output_dir, f"range_{i+1}")
        os.makedirs(range_dir, exist_ok=True)
        print(f"\n=== Диапазон {i+1}: {min_size}x{max_size}, цель: {need_count} шт ===")
        cleanup_directory(range_dir)
        downloaded_count = 0
        attempts = 0

        while downloaded_count < need_count and attempts < 6:
            attempts += 1
            keyword = random.choice(keywords)
            request_num = max(1, (need_count - downloaded_count) * (2 if attempts == 1 else 1))
            print(f"Попытка {attempts}: ищем '{keyword}' ({request_num} шт)")
            try:
                crawler = BingImageCrawler(
                    storage={'root_dir': range_dir},
                    feeder_threads=3,
                    parser_threads=3,
                    downloader_threads=6
                )
                crawler.crawl(keyword=keyword, max_num=request_num, file_idx_offset='auto')
            except Exception as e:
                print(f"Ошибка скачивания: {e}")
                continue

            cleanup_directory(range_dir)

            new_files = []
            for file_path in Path(range_dir).rglob("*.*"):
                try:
                    if not file_path.is_file():
                        continue
                    if file_path.suffix.lower() not in image_exts:
                        continue
                    if file_path.stat().st_size <= 10240:
                        continue
                    if not image_matches_size(str(file_path), min_size, max_size):
                        continue
                    abs_p = str(file_path.absolute())
                    if abs_p not in all_abs:
                        rel_p = str(file_path.relative_to(output_dir))
                        new_files.append((abs_p, rel_p))
                        all_abs.add(abs_p)
                except:
                    continue

            added = min(len(new_files), need_count - downloaded_count)
            all_files.extend(new_files[:added])
            downloaded_count += added
            print(f"Добавлено: {added}, всего {downloaded_count}/{need_count}")

            if downloaded_count < need_count:
                time.sleep(1)
                print("Недостаточно, пробуем снова...")

        print(f"Диапазон {i+1} завершён: {downloaded_count} изображений")

    return all_files

def create_annotation(files, annotation_file):
    with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(files)
    print(f"\nАннотация сохранена в {annotation_file}, всего файлов: {len(files)}")

def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений fish с диапазонами размеров")
    parser.add_argument('--output_dir', type=str, default='fish_images')
    parser.add_argument('--annotation_file', type=str, default='fish_annotation.csv')
    parser.add_argument('--size_ranges', type=str, required=True,
                        help='Диапазоны размеров через запятую, пример: "300x300,500x500,700x700"')
    parser.add_argument('--min_images', type=int, default=50)
    parser.add_argument('--max_images', type=int, default=1000)
    args = parser.parse_args()

    size_ranges = []
    for item in args.size_ranges.split(','):
        try:
            a, b = map(int, item.lower().split('x'))
            if a > b:
                a, b = b, a
            size_ranges.append((a, b))
        except:
            print(f"Ошибка формата диапазона: {item}")
            return

    print(f"Диапазоны размеров: {size_ranges}")

    total_min = max(50, args.min_images)
    total_max = min(1000, args.max_images)
    counts = generate_random_counts(size_ranges, total_min, total_max)
    print(f"Количество изображений по диапазонам (сумма ≤ 1000): {counts}, всего = {sum(counts)}")

    downloaded = download_images(args.output_dir, size_ranges, counts)
    if not downloaded:
        print("Не удалось скачать ни одного изображения!")
        return

    create_annotation(downloaded, args.annotation_file)

    print("\nПервые 5 файлов из аннотации:")
    it = ImageIterator(annotation_file=args.annotation_file)
    for idx, row in zip(range(5), it):
        print(row['relative_path'])

if __name__ == "__main__":
    main()