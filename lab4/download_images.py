# download_images.py
import csv
import os
import argparse
from icrawler.builtin import BingImageCrawler


class FileIterator:

    def __init__(self, source: str) -> None:
        self.files = []

        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    self.files.append(os.path.join(root, file))

        elif os.path.isfile(source):
            with open(source, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[0] != "":
                        self.files.append(row[0])

        else:
            raise ValueError(
                "Необходимо указать файл аннотации или папку с изображениями"
            )

        self.index = 0

    def __iter__(self) -> "FileIterator":
        return self

    def __next__(self) -> str:
        if self.index < len(self.files):
            path = self.files[self.index]
            self.index += 1
            return path
        raise StopIteration


def parse_args() -> argparse.Namespace:
    """
    Парсинг параметров с консоли
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="Путь к папке для сохранения изображений",
    )
    parser.add_argument(
        "--keywords",
        "-k",
        nargs="+",
        type=str,
        required=True,
        help="Ключевое слово для скачивания изображений",
    )
    parser.add_argument(
        "--annotation",
        "-a",
        type=str,
        default="annotation.csv",
        help="Файл для записи путей к загруженным файлам",
    )
    parser.add_argument(
        "--result",
        "-r",
        type=str,
        required=False,
        help="Путь к папке, где будут сохранены измененные изображения",
    )
    parser.add_argument(
        "--histogram",
        "-g",
        type=str,
        default="histogram.png",
        help="Путь для сохранения гистограммы",
    )
    parser.add_argument(
        "--dataframe",
        "-d",
        type=str,
        default="dataframe.csv",
        help="Путь для сохранения DataFrame'а",
    )
    return parser.parse_args()


def download_images(output_dir: str, keywords: set) -> None:
    """Скачивание изображений по ключевым словам в заданную директорию"""
    for kword in keywords:
        category_dir = os.path.join(output_dir, kword)
        os.makedirs(category_dir, exist_ok=True)

        crawler = BingImageCrawler(
            storage={"root_dir": category_dir}, downloader_threads=4
        )
        crawler.crawl(keyword=kword)


def create_annotation(output_dir: str, annotation_file: str) -> None:
    """Создание .csv файла, в котором располагаются пути к скачанным файлам"""
    with open(annotation_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = os.path.relpath(abs_path)
                writer.writerow([abs_path, rel_path])
