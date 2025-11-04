import argparse
import requests
from icrawler.builtin import GoogleImageCrawler


"""
Скачать изображения по ключевому слову "turtle", 
пользователь задаёт несколько цветов из списка на выбор. 
Количество изображений каждого цвета одинаковое.
"""


class Iterator:
    pass


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
        google_crawler = GoogleImageCrawler (
            downloader_threads=4, storage={"root_dir": f"{images_dir}/{color}"}
        )
        search_keyword = f"{color} {keyword}"
        google_crawler.crawl(search_keyword, max_num=100)


def create_annotation() -> None:
    pass


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
    output_folder = arguments_parse().output_folder
    annotation = arguments_parse().annotation
    avaible_colors = ["green", "black", "brown", "yellow"]
    
    colors = get_color(avaible_colors)
    image_parse(output_folder, colors, "turtle")


if __name__ == "__main__":
    main()