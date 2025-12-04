import argparse
import os
import csv

from icrawler.builtin import BingImageCrawler


def parsing() -> tuple[str, str]:
    """передача аргументов через командную строку"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("annotation_path", type=str)
    args = parser.parse_args()
    return args.file_path, args.annotation_path


def download_images(filename_images: str) -> None:
    """Скачивание картинок"""
    if os.path.exists(filename_images) == 0:
        os.mkdir(filename_images)
    while len(os.listdir(filename_images)) < 50:
        Bing_crawler = BingImageCrawler(storage={"root_dir": filename_images})
        Bing_crawler.crawl(
            keyword="dog",
            filters=dict(color="gray"),
            max_num=1000,
        )


def make_annotation_file(filename_annotation: str, filename_images: str) -> None:
    """Создание и запись файла аннотации"""
    if os.path.exists(filename_images):
        with open(filename_annotation, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Absolute Path", "Relative Path"])
            for i in os.listdir(filename_images):
                path = os.path.join(filename_images, i)
                path_full = os.path.abspath(path)
                writer.writerow([path_full, path])


class Path_Iterator:
    """Итератор по пути"""

    def __init__(self, source: str):
        self.items = []
        self.counter = 0
        if os.path.isfile(source):
            with open(source, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.items.append(row)
        else:
            for file in os.listdir(source):
                path = os.path.join(source, file)
                path_full = os.path.abspath(path)
                self.items.append([path_full, path])

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.items):
            path = self.items[self.counter]
            self.counter += 1
            return path[0]
        else:
            raise StopIteration


def main():
    try:
        filename_images, filename_annotation = parsing()
        download_images(filename_images)
        make_annotation_file(filename_annotation, filename_images)
        for path in Path_Iterator(filename_annotation):
            print(path)
    except Exception as ex:
        print("Ошибка: ", ex)


if __name__ == "__main__":
    main()
