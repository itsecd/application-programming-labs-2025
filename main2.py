import argparse
import os
import csv
import time

from icrawler.builtin import BingImageCrawler


def parsing() -> tuple[str, str, int]:
    """
    Передача аргументов через командную строку
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="Путь к папке для сохранения изображений")
    parser.add_argument("annotation_path", type=str, help="Путь к файлу аннотации")
    parser.add_argument("--time_limit", type=int, default=30, help="Ограничение по времени в секундах")
    args = parser.parse_args()
    return args.file_path, args.annotation_path, args.time_limit


def download_images(filename_images: str, time_limit: int) -> float:
    """
    Скачивание картинок по ключевому слову 'pig' с ограничением по времени
    """
    if not os.path.exists(filename_images):
        os.makedirs(filename_images)
    
    start_time = time.time()
    downloaded_count = 0
    
    while time.time() - start_time < time_limit and len(os.listdir(filename_images)) < 50:
        Bing_crawler = BingImageCrawler(storage={"root_dir": filename_images})
        Bing_crawler.crawl(
            keyword="pig",
            max_num=100,
        )
        
        current_count = len(os.listdir(filename_images))
        if current_count > downloaded_count:
            downloaded_count = current_count
            print(f"Скачано {downloaded_count} изображений...")
        
        time.sleep(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def make_annotation_file(filename_annotation: str, filename_images: str) -> None:
    """
    Создание и запись файла аннотации
    """
    with open(filename_annotation, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Absolute Path", "Relative Path"])
        for i in os.listdir(filename_images):
            path = os.path.join(filename_images, i)
            path_full = os.path.abspath(path)
            path_rel = os.path.relpath(path)
            writer.writerow([path_full, path_rel])


class Path_Iterator:
    """
    Итератор по пути
    """
    def __init__(self, source: str):
        self.items = []
        self.counter = 0
        if os.path.isfile(source):
            with open(source, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.items.append(row)
        else:
            for file in os.listdir(source):
                path = os.path.join(source, file)
                path_rel = os.path.relpath(path)
                path_full = os.path.abspath(path)
                self.items.append([path_full, path_rel])

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.items):
            path = self.items[self.counter]
            self.counter += 1
            return path
        else:
            raise StopIteration


def main():
    filename_images, filename_annotation, time_limit = parsing()
    
    print(f"Начинаем скачивание изображений по ключевому слову 'pig'...")
    print(f"Ограничение по времени: {time_limit} секунд")
    print(f"Минимальное количество изображений: 50")
        
    elapsed_time = download_images(filename_images, time_limit)
        
    make_annotation_file(filename_annotation, filename_images)
        
    final_count = len(os.listdir(filename_images))
    print(f"\nЗавершено скачивание:")
    print(f"Общее количество скачанных изображений: {final_count}")
    print(f"Затраченное время: {elapsed_time:.2f} секунд")

    print("\nСписок скачанных изображений:")
    for path in Path_Iterator(filename_annotation):
        print(path)

if __name__ == "__main__":
    main()