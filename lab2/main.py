import argparse
import csv
import os
from icrawler.builtin import BingImageCrawler


class FileIterator:
    def __init__(self, annotation_file=None, images_dir=None) -> None:
        self.root_dir = root_dir
        self.files = []

    def __iter__(self):
        return self

    def __next__(self):

        if self.counter < self.limit:
            self.counter += 1
            return self.counter
        else:
            raise StopIteration



def create_annotation(output_dir, annotation_file) -> None:

    with open(annotation_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Abs path", "Rel path"])
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = os.path.relpath(abs_path)
                writer.writerow([abs_path, rel_path])

def parse_args() -> argparse.Namespace:
    """
    Парсинг параметров с консоли
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",
                        "-o",
                        type=str,
                        required=True,
                        help="Путь к папке для сохранения изображений")
    parser.add_argument("--keywords",
                        "-k",
                        nargs='+',
                        type=str,
                        required=True,
                        help="Ключевое слово для скачивания изображений")
    parser.add_argument("--annotation",
                        "-a",
                        type=str,
                        default="annotation.csv",
                        help="Файл для записи путей к загруженным файлам")
    return parser.parse_args()


def download_images(output_dir=str, keywords=set) -> None:
    """Скачивание изображений по ключевым словам в заданную директорию """
    for kword in keywords:
        category_dir = os.path.join(output_dir, kword)
        os.makedirs(category_dir, exist_ok=True)

        crawler = BingImageCrawler(storage={'root_dir': category_dir}, downloader_threads=4)
        crawler.crawl(keyword=kword, max_num=2)


def main() -> None:
    """"""
    args = parse_args()
    download_images(args.output, args.keywords)
    create_annotation(args.output, args.annotation)


if __name__ == "__main__":
    main()
