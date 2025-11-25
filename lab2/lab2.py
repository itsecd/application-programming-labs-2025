import argparse
import csv
import os
from icrawler.builtin import BingImageCrawler



def read_arguments():
    """
    Чтение и парсинг аргументов командной строки.
    
    Returns:
        argparse.Namespace: Объект с аргументами командной строки
    """
    parser = argparse.ArgumentParser(
        description="Download multiple horse images by keywords and annotate paths."
    )
    parser.add_argument("--folder", required=True, help="Directory for downloaded images")
    parser.add_argument("--csv", required=True, help="Target CSV file")
    parser.add_argument("--words", nargs="+", required=True, help="List of keywords")
    parser.add_argument("--count", type=int, required=True, help="Images per keyword")
    return parser.parse_args()


def generate_csv(csv_path, base_folder):
    """
    Генерация CSV файла с абсолютными и относительными путями к изображениям.
    
    Args:
        csv_path (str): Путь для сохранения CSV файла
        base_folder (str): Базовая папка для поиска изображений
    """
    root_origin = os.path.dirname(os.path.abspath(csv_path))

    rows = []
    for root, _, files in os.walk(base_folder):
        for name in files:
            abs_p = os.path.abspath(os.path.join(root, name))
            rel_p = os.path.relpath(abs_p, start=root_origin)
            rows.append((abs_p, rel_p))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path"])
        writer.writerows(rows)


class PathCSVIterator:
    """
    Итератор для чтения путей из CSV файла.
    
    Attributes:
        items (list): Список абсолютных путей из CSV
        i (int): Текущий индекс итерации
    """
    
    def __init__(self, csv_path):
        """
        Инициализация итератора с загрузкой данных из CSV.
        
        Args:
            csv_path (str): Путь к CSV файлу
        """
        with open(csv_path, encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)
            self.items = [row[0] for row in r]
        self.i = 0

    def __iter__(self):
        """
        Возвращает сам объект как итератор.
        
        Returns:
            PathCSVIterator: Сам объект итератора
        """
        return self

    def __next__(self):
        """
        Возвращает следующий элемент итератора.
        
        Returns:
            str: Следующий абсолютный путь из CSV
            
        Raises:
            StopIteration: Когда элементы закончились
        """
        if self.i >= len(self.items):
            raise StopIteration
        val = self.items[self.i]
        self.i += 1
        return val


def run():
    """
    Основная функция выполнения программы.
    
    Выполняет загрузку изображений, генерацию CSV и демонстрацию работы итератора.
    """
    args = read_arguments()

    crawler = BingImageCrawler(storage={"root_dir": args.folder})

    for keyword in args.words:
        print(f"Downloading images for: {keyword}")
        crawler.crawl(
            keyword=keyword,
            max_num=args.count
        )

    generate_csv(args.csv, args.folder)

    print("\n=== CSV Iterator Example ===")
    for path in PathCSVIterator(args.csv):
        print(path)


if __name__ == "__main__":
    run()