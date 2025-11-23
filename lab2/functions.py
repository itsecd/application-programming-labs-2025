import csv
import os
from math import ceil

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


def download_images(ranges: list, path_d: str) -> None:
    """
    установка изображений
    """

    min_all_images = 50
    need_for_range = ceil(min_all_images / len(ranges))
    attempts = 5
    images_now = 0

    for i in range(len(ranges)):
        crawler = BingImageCrawler(
            feeder_threads=8,
            parser_threads=8,
            downloader_threads=12,
            storage={'root_dir': path_d}
        )

        for _ in range(attempts):
            if images_now >= need_for_range * (i + 1):
                break

            crawler.crawl(
                offset=images_now,
                keyword='dog',
                max_num=need_for_range * (i + 1),
                min_size=ranges[i][0],
                max_size=ranges[i][1]
            )

            images_now = len(os.listdir(path_d))


def parse_size_range(ranges: str) -> tuple:
    """
    получение диапазонов
    """

    sizes = ranges.split('-')

    min_size = sizes[0].split('x')
    max_size = sizes[1].split('x')

    min_h = int(min_size[1])
    min_w = int(min_size[0])

    max_h = int(max_size[1])
    max_w = int(max_size[0])

    if min_h > max_h:
        raise ValueError('минимальная высота больше максимальной')

    if min_w > max_w:
        raise ValueError('минимальная ширина больше максимальной')

    return (min_h, min_w), (max_h, max_w)
