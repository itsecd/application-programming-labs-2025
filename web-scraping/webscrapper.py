#!/usr/bin/env python3

from icrawler.builtin import GoogleImageCrawler

import csv
import os
import argparse
import random

class ImageIterator:
    def __init__(self, csv_file: str) -> None:
        self.path_list = []
        with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.path_list.append(row[0])
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.path_list):
            self.index += 1
            return self.path_list[self.index - 1]
        else:
            raise StopIteration


def create_annotation(csv_path: str, folder: str) -> None:
    """
    Создание CSV аннотации, абсолютные и относительные пути
    """
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])

        for root, _, files in os.walk(folder):
            for file in files:
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = os.path.relpath(os.path.join(root, file), folder)
                writer.writerow([abs_path, rel_path])
    
def args_parse() -> argparse.Namespace:
    """Парсинг аргументов"""
    parser = argparse.ArgumentParser(description="Скачивание изображений и создание аннотации CSV")
    parser.add_argument("--folder", required=True, help="Папка для сохранения изображений")
    parser.add_argument("--csv", required=True, help="CSV файл аннотации")
    parser.add_argument("--color", choices=["red", "yellow", "green", "blue"], required=True, help="Цвет изображений")
    return parser.parse_args()


def main() -> None:
    """Главная функция"""
    args = args_parse()

    google_crawler = GoogleImageCrawler(storage={'root_dir': args.folder})
    
    max_num = random.randint(50, 1000)
    google_crawler.crawl(keyword='bird', max_num=max_num, filters={"color": args.color})

    create_annotation(args.csv, args.folder)

    # Проверка работы итератора
    for path in ImageIterator(args.csv):
        print(path)


if __name__ == "__main__":
    main()