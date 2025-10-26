from icrawler.builtin import GoogleImageCrawler
import os
import csv
import argparse


def download_images(filename_imagesdata: str) -> None:
    """
    Скачивание картинок
    """
    while len(os.listdir(filename_imagesdata)) < 50:
        Google_crawler = GoogleImageCrawler(storage={"root_dir": filename_imagesdata})
        Google_crawler.crawl(
            keyword="monkey",
            filters=dict(date=((2025, 1, 1), (2025, 12, 31))),
            max_num=1000,
        )


def make_annotation_file(filename_annotation: str, filename_imagesdata: str) -> None:
    """
    Создание и запись файла аннотации
    """
    with open(filename_annotation, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for f in os.listdir(filename_imagesdata):
            path_full = os.path.abspath(f)
            path = os.path.join(filename_imagesdata, f)
            writer.writerow([path_full, path])


class Path_Iterator:
    def __init__(self, source):
        if os.path.isfile(source):
            with open(source, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.items = [row for row in reader]
                self.counter = 0
        else:
            for f in source:
                path_full = os.path.abspath(f)
                path = os.path.join(source, f)
                self.items.append([path_full,path])
            self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.items):
            path = self.items[self.counter]
            self.counter += 1
            return path
        else:
            raise StopIteration


def parsing() -> tuple[str, str]:
    """
    передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenameimagesdata", type=str)
    parser.add_argument(
        "filenameannotation", type=str)
    args = parser.parse_args()
    return args.filenameimagesdata, args.filenameannotation


def main() -> None:
    try:
        filename_imagesdata, filename_annotation = parsing()
        download_images(filename_imagesdata)
        make_annotation_file(filename_annotation, filename_imagesdata)
        for path in Path_Iterator(filename_annotation):
            print(path)
    except Exception as exp:
        print(exp)


if __name__ == "__main__":
    main()

