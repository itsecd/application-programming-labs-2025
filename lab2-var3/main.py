from __future__ import annotations
import argparse
import csv
from typing import List, Tuple

from downloader import download_images
from iterator import ImageIterator
from utils import generate_random_counts


def create_annotation(files: List[Tuple[str, str]], annotation_file: str) -> None:
    """
    Создаёт CSV-файл аннотации.
    """
    with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(files)


def main() -> None:
    """
    Основная функция CLI: скачивает изображения, создаёт аннотацию,
    печатает первые 5 записей.
    """
    parser = argparse.ArgumentParser(description="Скачивание изображений рыб по диапазонам размеров")
    parser.add_argument('--output_dir', type=str, default='fish_images')
    parser.add_argument('--annotation_file', type=str, default='fish_annotation.csv')
    parser.add_argument('--size_ranges', type=str, required=True,
                        help='Например: "300x300,500x500,700x700"')
    parser.add_argument('--min_images', type=int, default=50)
    parser.add_argument('--max_images', type=int, default=1000)

    args = parser.parse_args()

    size_ranges: List[Tuple[int, int]] = []
    for item in args.size_ranges.split(','):
        try:
            a, b = map(int, item.lower().split('x'))
            if a > b:
                a, b = b, a
            size_ranges.append((a, b))
        except ValueError:
            return

    total_min = max(50, args.min_images)
    total_max = min(1000, args.max_images)

    counts = generate_random_counts(size_ranges, total_min, total_max)
    downloaded = download_images(args.output_dir, size_ranges, counts)

    if not downloaded:
        return

    create_annotation(downloaded, args.annotation_file)

    it = ImageIterator(annotation_file=args.annotation_file)

    for idx, row in zip(range(5), it):
        print(row['relative_path'])


if __name__ == "__main__":
    main()