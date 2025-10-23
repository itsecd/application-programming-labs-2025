import csv
import os
import random
import argparse
from icrawler.builtin import BingImageCrawler


def icrawler(dirname: str, num_val: int, max_val: list[int], min_val: list[int]) -> None:
    """
    Выполняет скачивание картинок из инернета
    по кодовому слову fish
    """
    bing_crawler = BingImageCrawler(storage={'root_dir': dirname}, downloader_threads=1, feeder_threads=1, parser_threads=1)
    bing_crawler.downloader.retry_num = 1
    bing_crawler.crawl(keyword='fish', max_num=num_val, max_size=max_val, min_size=min_val)


def inputer():
    """
    Принимает пользовательский ввод максимального
    и минимального размера картинки
    """
    list_max = []
    list_min = []
    while True:

        max_height = int(input("Введите максимальную высоту картинки "))
        max_width = int(input("Введите максимальную ширину картинки "))
        min_height = int(input("Введите минимальную высоту картинки "))
        min_width = int(input("Введите минимальную ширину картинки "))

        if (max_height > 0 and max_width > 0 and
        min_height > 0 and min_width > 0 and
        max_height > min_height and max_width > min_width):

            list_max.append([max_height, max_width])
            list_min.append([min_height, min_width])
        else:
            print("Ошибка: минимальные размеры должны быть меньше максимальных и все размеры > 0 ")

        flag = int(input("Хотите продолжить? 0 если нет, иначе да "))
        if flag == 0:
            break
    return list_max, list_min


def task_icrawler(max_num: int, dirname: str):
    """
    просит запрос от пользователя и выполняет функцию
    icrawler исходя из этих запросов
    """
    if max_num < 50 or  max_num > 1000:
        raise ValueError("Error. Value is not correct.")
    list_max, list_min = inputer()
    for i in range (len(list_max)):
        icrawler(dirname, max_num//len(list_max), list_max[i], list_min[i])


def get_paths(dirpath: str)->list[list[str]]:
    """
    получает пути из директории
    """
    if not os.path.exists(dirpath):
        return []

    dir_path = os.getcwd()
    paths = []
    for file in os.listdir(dirpath):
        real_path = os.path.join(dirpath, file)
        paths.append([os.path.abspath(real_path), os.path.relpath(real_path, dir_path)])
    return paths


def go_to_csv(filename: str, data: list[str])->None:
    """
    записывает строки из списка в csv файле
    """
    head =  [['Абсолбтный путь, Относительный путь']]
    data = head + data
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, "w", newline='', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


class MyIterator:
    def __init__(self, filepath: str):
        try:
            self.filepath = filepath
            self.file = open(filepath, "r", encoding = "utf-8")
        except Exception as e:
            print(f"Error: {e}")

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()

        if not line:
            self.file.close()
            raise StopIteration

        return line

def main():
    parser = argparse.ArgumentParser(description="Извлечение данных из файла на основе шаблонов.")
    parser.add_argument("--directory", "-d", default="image", type=str, help="Путь к дирректории.")
    parser.add_argument("--csvfile", "-c", default="data.csv", type=str, help="Путь к файлу для записи результата.")
    parser.add_argument("--count", "-n", default=300, type=int, help="Количество картинок")
    args = parser.parse_args()


    task_icrawler(args.count, args.directory)

    path_list = get_paths(args.directory)

    go_to_csv(args.csvfile, path_list)

    iter = MyIterator(args.csvfile)
    for i in iter:
        print(i, end = "")

if __name__ == "__main__":
    main()