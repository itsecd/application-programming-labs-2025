import csv
import argparse
import os
import random
from icrawler.builtin import BingImageCrawler # type: ignore

class path_iterator:
    """Итератор по путям"""
    def __init__ (self, source: str) -> None:
        self.paths = []
        self.counter = 0
        if (source.endswith('.csv')):
            with open(source, mode='r', newline='', encoding='utf-8') as file:
             reader = csv.reader(file)
             next(reader)
             for row in reader:
               self.paths.append(row[0])
        else:
            for filename in os.listdir(source):
                self.paths.append(os.path.join(source,filename))
         
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.counter < len (self.paths)):
            path = self.paths[self.counter]
            self.counter +=1
            return path
        else:
            raise StopIteration

def arguments () -> argparse.Namespace:
     """Парсинг аргументов строки"""
     parser = argparse.ArgumentParser( description="Скачивание изображений по ключевому слову с заданными размерами")
     parser.add_argument('--min_width', type=int, required=True, help="Минимальная ширина")
     parser.add_argument('--max_width', type=int, required=True, help="Максимальная ширина")
     parser.add_argument('--min_height', type=int, required=True, help="Минимальная высота")
     parser.add_argument('--max_height', type=int, required=True, help="Максимальная высота")
     parser.add_argument('--output_folder', type=str, required=True, help="Выходная дирректория")
     parser.add_argument('--csv_path', type=str, required=True, help="Пусть csv файла")
     return parser.parse_args()

def downloader(minimum_size: tuple[int, int], maximum_size: tuple[int, int], output: str) ->None:
     """Качает изображения и сохраняет их"""
     if not(os.path.exists(output)):
        os.mkdir(output)
     maxi_num = random.randint(50,1000)
     bing_crawler = BingImageCrawler(storage={'root_dir': output})
     bing_crawler.crawl(keyword='cat', max_num=maxi_num)
     img_filter(output, minimum_size, maximum_size)

def img_filter(output: str, minimum_size: tuple[int, int], maximum_size: tuple[int, int]) -> None:
    """Сортировка по размеру"""
    from PIL import Image # pyright: ignore[reportMissingImports]
    for filename in os.listdir(output):
      filepath = os.path.join(output, filename)
      try:
          with Image.open(filepath) as img:
             width, height = img.size
             min_width, min_height = minimum_size
             max_width, max_height = maximum_size
             if not (min_width <= width <= max_width and min_height <= height <= max_height):
                 os.remove(filepath)
      except:
       print(f"Ошибка при проверке {filepath}")
       os.remove(filepath)


def create_csv(output: str, csv_path: str) -> None:
    """Создание Csv анотации"""
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute path', 'relative path'])
        for filename in os.listdir(output):
          abs_path = os.path.abspath(os.path.join(output, filename))
          rel_path = os.path.join(output, filename)
          writer.writerow([abs_path, rel_path])

def main() -> None:
    """Основная функция"""
    args = arguments()
    min_size = (args.min_width, args.min_height)
    max_size = (args.max_width, args.max_height)
    downloader(min_size, max_size, args.output_folder)
    create_csv(args.output_folder, args.csv_path)

if __name__ == '__main__':
     main()