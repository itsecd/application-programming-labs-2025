import argparse
import csv
import os
import random
from icrawler.builtin import BingImageCrawler

class AnnotationIterator:
    def __init__(self, annotation_path: str):
        self.items = []
        with open(annotation_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.items.append(row)

    def __iter__(self):
        return iter(self.items)


def validate_annotation_path(path: str):
    if not path.endswith(".csv"):
        raise ValueError("файл аннотации должен иметь расширение .csv")



def clear_directory(directory: str):
    """
    очистка директории
    """
    if not os.path.exists(directory):
        return
    for file in os.listdir(directory):
        full = os.path.join(directory, file)
        if os.path.isfile(full):
            os.remove(full)


def download_snakes_with_colors(colors: list, directory: str, min_total: int = 50):
    """
    скачивание с распределением цветов по папкам
    """

    color_dirs = {}
    for color in colors:
        color_dir = os.path.join(directory, color)
        os.makedirs(color_dir, exist_ok=True)
        color_dirs[color] = color_dir
        clear_directory(color_dir)

    remaining = min_total + 1
    color_counts = {}

    for i, color in enumerate(colors[:-1]):
        count = random.randint(1, max(1, remaining // 2))
        color_counts[color] = count
        remaining -= count

    color_counts[colors[-1]] = remaining

    print("распределение по цветам:")
    for color, count in color_counts.items():
        print(f"  {color}: {count} изображений")

    total_downloaded = 0
    for color, count in color_counts.items():
        if count <= 0:
            continue

        print(f"скачиваю {count} изображений: snake {color}")

        crawler = BingImageCrawler(storage={"root_dir": color_dirs[color]})
        crawler.crawl(
            keyword=f"snake {color}",
            max_num=count
        )

        downloaded = len(os.listdir(color_dirs[color]))
        total_downloaded += downloaded
        print(f" скачано: {downloaded}")

    print(f"всего скачано: {total_downloaded} изображений")
    return total_downloaded


def create_annotation(csv_path: str, directory: str):
    """
    создание CSV аннотации
    """
    rows = []
    for color_dir in os.listdir(directory):
        color_path = os.path.join(directory, color_dir)
        if os.path.isdir(color_path):
            for filename in os.listdir(color_path):
                abs_path = os.path.abspath(os.path.join(color_path, filename))
                rel_path = os.path.join(directory, color_dir, filename)
                rows.append([abs_path, rel_path, color_dir])

    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path", "color"])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="скачивание изображений змей по цветам"
    )

    parser.add_argument("directory", type=str, help="папка для изображений")
    parser.add_argument("annotation", type=str, help="CSV-файл аннотации")
    parser.add_argument("colors", nargs="+", help="цвета: red green blue ...")
    parser.add_argument("--min", type=int, default=50, help="минимальное количество изображений (по умолчанию 50)")

    args = parser.parse_args()

    try:
        validate_annotation_path(args.annotation)

        os.makedirs(args.directory, exist_ok=True)
        clear_directory(args.directory)

        download_snakes_with_colors(args.colors, args.directory, args.min)

        create_annotation(args.annotation, args.directory)

        print("\nаннотация готова. пути:\n")
        for item in AnnotationIterator(args.annotation):
            print(item)

    except Exception as e:
        print("ошибка:", e)


if __name__ == "__main__":
    main()
