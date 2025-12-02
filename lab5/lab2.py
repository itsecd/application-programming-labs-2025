import argparse
import csv
import os

from icrawler.builtin import BingImageCrawler


class FileIterator:
    def __init__(self, filepath: str):
        try:
            self.filepath = filepath
            self.file = open(filepath, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f'File {filepath} not found.')

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()

        if not line:
            self.file.close()
            raise StopIteration

        return line


def get_color(avaible_colors: list[str]) -> list[str]:
    """Данная функция обрабатывает выбор пользователя"""
    print(f"Доступные цвета {avaible_colors}")
    user_input = input("Введите цвета через запятую: ").strip()

    selected_colors = [color.strip().lower() for color in user_input.split(',')]
    valid_colors = [color for color in selected_colors if color in avaible_colors]

    if valid_colors:
        return valid_colors
    else:
        return [avaible_colors[0]]


def image_parse(images_dir: str, colors: list[str], keyword: str) -> None:
    """
    Данная функция находит изображения по ключевому слову с указынным фильтром
    и сохраняет их в директорию images_dir
    """
    for color in colors:
        bing_crawler = BingImageCrawler (
            downloader_threads=4, storage={"root_dir": f"{images_dir}/{color}"}
        )
        search_keyword = f"{keyword} {color}"
        bing_crawler.crawl(search_keyword, max_num=4)


def get_paths(dir_path: str) -> list[list[str]]:
    """
    Данная функция вовзращает список всех абсолютных
    и относительных путей к изображениям
    """
    if os.path.exists(dir_path):
        paths = [["Абсолютный путь", "Относительный путь"]] 

        for dir in os.listdir(dir_path):   
            for file in os.listdir(f"{dir_path}\\{dir}"):
                paths.append([os.path.abspath(f"{dir_path}\{dir}\{file}"), 
                              f"{dir_path}\{dir}\{file}"])

        return paths
    else:
        return []


def create_annotation(file_name: str, img_paths: list[list[str]]) -> None:
    """Данная функция создаёт аннотацию в виде csv-файла"""
    with open(file_name, 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(img_paths)


def arguments_parse() -> argparse.Namespace:
    """Данная функция получает аргументы(output_folder, annotation) из командной строки"""
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output_folder", help="Папка, в которую необходимо сохранять найденные изображения")
    parser.add_argument("-a", "--annotation", help="Имя csv файла аннотации")

    args = parser.parse_args()

    if (args.output_folder and args.annotation) is not None:
        return args
    else:
        raise Exception("The name of output image folder and the annotation file can't be None")


def main() -> None:
    images_dir = arguments_parse().output_folder
    annotation = arguments_parse().annotation
    avaible_colors = ["green", "black", "brown", "yellow"]

    colors = get_color(avaible_colors)
    image_parse(images_dir, colors, "turtle")
    paths = get_paths(images_dir)    

    create_annotation(annotation, paths)
    
    it = FileIterator(annotation)
    print(it[2])
    

if __name__ == "__main__":
    main()