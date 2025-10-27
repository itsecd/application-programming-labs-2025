import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler


class PathsIterator:
    def __init__(self, path: str):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.paths = [row for row in reader]
            self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < len(self.paths):
            self.count += 1
            return self.paths[self.count]
        else:
            raise StopIteration


# def parse_arguments() -> str:
#     """
#     Парсинг аргументов из командной строки
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument("input", type=str, help="input file path")
#     args = parser.parse_args()
#     return args.input


def colors_choice() -> list[str]:
    user_choice = -1
    while user_choice != 0:
        colors = list[str]()
        print(
            "\n\nВыберите цвета изображений черепах:\n"
            "1)Green\n"
            "2)Blue\n"
            "3)Yellow\n"
            "4)Brown\n"
            "5)Grey\n"
            "6)Black&White\n"
            "0)Готово\n\n"
            "Выбраны: "
        )
        for i in colors:
            print(i+", ")
        user_choice = int(input("\nВаш выбор: "))
        if user_choice == 1:
            if colors.__contains__("green"):
                colors.remove("green")
            else:
                colors.append("green")
    return colors


def turtle_crawler(path: str, num: int, colors: list[str]) -> None:
    google_crawler = GoogleImageCrawler(storage={"root_dir": path})
    for i in colors:
        google_crawler.crawl(keyword="turtle " + i, max_num=num//len(colors))


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
        colors = colors_choice()
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        turtle_crawler(img_path, num, colors)
        table = get_paths(img_path)
        print(table)
        annotation_maker(annotation_path, table)
        # iter = PathsIterator(annotation_path)
        # for i in iter:
        #     print(i)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()
