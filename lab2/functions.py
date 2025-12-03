import csv
import os

from icrawler.builtin import BingImageCrawler
from PIL import Image


class AnnotationIterator:
    def __init__(self, annotation_name: str):
        """
        итератор путей
        """
        paths = []

        with open(annotation_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                paths.append(row)

        self.Paths = paths[1:]

    def __iter__(self):
        return iter(self.Paths)


def annotation_check(path_a: str) -> None:
    """
    проверка csv
    """
    if not path_a.endswith('.csv'):
        raise ValueError('файл аннотации должен иметь расширение .csv')


def write_csv(path_annotation: str, path_directory: str) -> None:
    """
    создание файла аннотации
    """
    data = []

    for image_name in os.listdir(path_directory):
        absolute_path = os.path.abspath(os.path.join(path_directory, image_name))
        relative_path = os.path.join(path_directory, image_name)
        data.append([absolute_path, relative_path])

    with open(path_annotation, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])
        writer.writerows(data)


def clear_dir(path_d: str) -> None:
    """
    очистка папки
    """
    if not os.path.exists(path_d):
        return

    for filename in os.listdir(path_d):
        file_path = os.path.join(path_d, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def make_grayscale(path_d: str) -> None:
    """
    перевод в полутон
    """
    for file in os.listdir(path_d):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
            path = os.path.join(path_d, file)
            img = Image.open(path).convert('L')
            img.save(path)


def download_images(path_d: str, total_images: int = 50) -> None:
    """
    скачивание изображений 
    """
    crawler = BingImageCrawler(
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=2,
        storage={'root_dir': path_d}
    )

    crawler.downloader.delay = 1.0

    crawler.crawl(
        keyword='dog',
        max_num=total_images,
        offset=0
    )
