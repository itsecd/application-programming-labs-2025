import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler

# def parse_arguments() -> str:
#     """
#     Парсинг аргументов из командной строки
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument("input", type=str, help="input file path")
#     args = parser.parse_args()
#     return args.input


def turtle_crawler(path: str, num: int) -> None:
    google_crawler = GoogleImageCrawler(storage={"root_dir": path})
    google_crawler.crawl(keyword="turtle", max_num=num)


def get_paths(dir_path: str) -> list[[str]]:
        os.chdir(dir_path)
        files = os.listdir()
        file_paths = [['Абсолютный путь:', 'Относительный путь:']]
        for i in files:
            file_paths.append([os.path.abspath(i), os.path.join(dir_path, i)])
        os.chdir("..")
        return file_paths


def annotation_maker(path: str, data: list[[str]]) -> None:
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main() -> None:
    try:
        img_path = "imgs"
        annotation_path = "annotation.csv"
        num = 3
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        turtle_crawler(img_path, num)
        table = get_paths(img_path)
        #print(table)
        annotation_maker(annotation_path, table)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()