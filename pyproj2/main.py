import argparse
import os
import csv

from icrawler.builtin import GoogleImageCrawler
from math import ceil


class AnnotationIterator:
    def __init__(self, annotation_name: str):
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
    прооверка является ли имя файла csv файлом
    """

    if path_a[-4:] != '.csv':
        raise ValueError('--file должен содержать csv файл')


def write_csv(path_a: str, path_d: str) -> None:
    """
    создание файла аннотации
    """

    data = [
        ['Абсолютный путь к файлу','Относительный путь к файлу']
    ]

    for image_name in os.listdir(path_d):
        absolute_path = os.path.join(os.getcwd(), path_d, image_name)
        relative_path = os.path.join(path_d, image_name)
        data.append([absolute_path, relative_path])

    with open(path_a, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def clear_dir(path_d: str) -> None:
    """
    очищает папку если она ужу существует
    """

    for filename in os.listdir(path_d):
        file_path = os.path.join(path_d, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def download_images(ranges: tuple, path_d: str) -> None:
    """
    установка изображений
    """

    min_all_images = 4
    need_for_range = ceil(min_all_images / len(ranges))
    attempts = 1
    images_now = 0

    crawler = GoogleImageCrawler(
        downloader_threads=4,
        storage={'root_dir': path_d}
    )

    for i in range(len(ranges)):
        for a in range(attempts):
            if images_now == need_for_range*(i+1):
                break
            crawler.crawl(
                offset=images_now,
                keyword='rabbit',
                max_num=need_for_range*(i+1),
                min_size=ranges[i][0],
                max_size=ranges[i][1]
            )

            images_now = len(os.listdir(path_d))


def parse_size_range(ranges: str) -> tuple:
    """
    получчение диапазонов
    """

    sizes = ranges.split('-')
    min_size = sizes[0].split('x')
    max_size = sizes[1].split('x')
    min_h = int(min_size[0])
    min_w = int(min_size[1])
    max_h = int(max_size[0])
    max_w = int(max_size[1])

    if min_h > max_h:
        raise ValueError('Минимальная высота изображения не может быть больше максимальной')
    if min_w > max_w:
        raise ValueError('Минимальная ширина изображения не может быть больше максимальной')

    return (min_h, min_w), (max_h, max_w)


def main():
    try:
        parser = argparse.ArgumentParser(description='Скачивает изображения по ключевому слову rabbit')
        parser.add_argument("--ranges", nargs='+', required=True, type=parse_size_range, help="Диапазоны размеров изображений в формате: minWxminH-maxWxmaxH. Например: 100x100-300x300 500x500-800x800")
        parser.add_argument("--directory", type=str, required=True, help="Путь до папки")
        parser.add_argument("--annotation", type=str, required=True, help="Путь до файла анотации")

        args = parser.parse_args()

        annotation = args.annotation.split('/')[-1]
        directory = args.directory.split('/')[-1]

        annotation_check(annotation)

        os.makedirs(directory, exist_ok=True)

        clear_dir(directory)

        download_images(args.ranges, directory)

        write_csv(annotation, directory)

        images_paths = AnnotationIterator(annotation)

        for image_path in images_paths:
            print(image_path)


    except IndexError:
        print('Ошибка в вводе --ranges')
    except ValueError as e:
        print(e)
    except NotADirectoryError:
        print('Ошибка в вводе --directory')

if __name__ == "__main__":
    main()