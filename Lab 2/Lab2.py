import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler


class PathsIterator:
    """
    Итератор по путям к файлам. Принимает путь к файлу аннотации как параметр конструктора
    """
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


def parse_arguments() -> list:
    """
    Парсинг аргументов из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img_dir", default="imgs", type=str, help="image folder path")
    parser.add_argument("-c", "--csv_path", default="annotation.csv", type=str, help="annotation file path")
    parser.add_argument("-n", "--img_max_num", type=int, default=50, help="max number of downloaded images")
    args = parser.parse_args()
    return [args.img_dir, args.csv_path, args.img_max_num]


def colors_choice() -> list[str]:
    """
    Выбор цветов для списка цветов изображений
    """
    user_choice = -1
    colors = list[str]()
    while user_choice != 0:
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
            print(i)
        user_choice = int(input("\nВаш выбор: "))
        if user_choice == 1:
            if colors.__contains__("green"):
                colors.remove("green")
            else:
                colors.append("green")
        elif user_choice == 2:
            if colors.__contains__("blue"):
                colors.remove("blue")
            else:
                colors.append("blue")
        elif user_choice == 3:
            if colors.__contains__("yellow"):
                colors.remove("yellow")
            else:
                colors.append("yellow")
        elif user_choice == 4:
            if colors.__contains__("brown"):
                colors.remove("brown")
            else:
                colors.append("brown")
        elif user_choice == 5:
            if colors.__contains__("grey"):
                colors.remove("grey")
            else:
                colors.append("grey")
        elif user_choice == 6:
            if colors.__contains__("black&white"):
                colors.remove("black&white")
            else:
                colors.append("black&white")
    return colors


def turtle_crawler(path: str, num: int, colors: list[str]) -> None:
    """
    Скачивание изображений
    """
    google_crawler = GoogleImageCrawler(storage={"root_dir": path})
    if len(colors) == 0:
        google_crawler.crawl(keyword="turtle", max_num=num)
    for i in colors:
        google_crawler.crawl(keyword="turtle " + i, max_num=num//len(colors))


def get_paths(dir_path: str) -> list[[str]]:
    """
    Создание таблицы путей к файлам
    """
    os.chdir(dir_path)
    files = os.listdir()
    file_paths = [["Абсолютный путь:", "Относительный путь:"]]
    for i in files:
        file_paths.append([os.path.abspath(i), os.path.join(dir_path, i)])
    os.chdir("..")
    return file_paths


def annotation_maker(path: str, data: list[[str]]) -> None:
    """
    Запись таблицы путей в файл аннотации
    """
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main() -> None:
    try:
        img_path, annotation_path, num = parse_arguments()
        colors = colors_choice()
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        turtle_crawler(img_path, num, colors)
        table = get_paths(img_path)
        annotation_maker(annotation_path, table)
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()
