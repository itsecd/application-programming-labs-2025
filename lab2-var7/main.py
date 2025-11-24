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
    скачивание + добор
    """
    downloaded = 0

    for color in colors:
        count = random.randint(1, 10)

        print(f"скачиваю {count} картинки: snake {color}")

        crawler = BingImageCrawler(storage={"root_dir": directory})
        crawler.crawl(
            keyword=f"snake {color}",
            max_num=count
        )

    downloaded = len(os.listdir(directory))

    while downloaded < min_total:
        need_one_color = random.choice(colors)
        print(f"догрузка: {need_one_color}")

        crawler = BingImageCrawler(storage={"root_dir": directory})
        crawler.crawl(
            keyword=f"snake {need_one_color}",
            max_num=1
        )

        downloaded = len(os.listdir(directory))


def create_annotation(csv_path: str, directory: str):
    """
    создание CSV аннотации
    """
    rows = []
    for filename in os.listdir(directory):
        abs_path = os.path.abspath(os.path.join(directory, filename))
        rel_path = os.path.join(directory, filename)
        rows.append([abs_path, rel_path])

    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path"])
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
