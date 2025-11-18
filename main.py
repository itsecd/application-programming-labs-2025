import argparse
import os
import sys
from datetime import datetime

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(__file__))

from image_crawler.image_downloader import download_images
from image_crawler.csv_annotator import create_annotation_csv
from image_crawler.iterators import ImagePathIterator


def main():
    parser = argparse.ArgumentParser(description='Скачивание изображений лошадей')
    parser.add_argument('--storage-dir', type=str, default='horses_images')
    parser.add_argument('--annotation-file', type=str, default='annotation.csv')
    parser.add_argument('--date-from', type=str, required=True)
    parser.add_argument('--date-to', type=str, required=True)
    parser.add_argument('--max-num', type=int, default=100)

    args = parser.parse_args()

    # Простая проверка дат (без сложной логики)
    try:
        datetime.strptime(args.date_from, '%Y-%m-%d')
        datetime.strptime(args.date_to, '%Y-%m-%d')
    except ValueError:
        print("Ошибка: используйте формат даты ГГГГ-ММ-ДД")
        return

    # Скачиваем изображения
    download_images(
        keyword='horse',
        date_from=args.date_from,
        date_to=args.date_to,
        max_num=args.max_num,
        save_dir=args.storage_dir
    )

    # Создаем аннотацию
    create_annotation_csv(args.storage_dir, args.annotation_file)

    # Демонстрируем итератор
    print("\nДемонстрация итератора (первые 5 путей):")
    iterator = ImagePathIterator(args.annotation_file)

    for i, path in enumerate(iterator):
        if i >= 5:
            break
        print(f"  {path}")

    print(f"\nВсего файлов: {len(iterator)}")


if __name__ == "__main__":
    main()