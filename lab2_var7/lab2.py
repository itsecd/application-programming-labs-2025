import os
import csv
import random
import argparse
import time

from icrawler.builtin import BingImageCrawler


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """

    parser = argparse.ArgumentParser(description='Скачивание изображений змей по цветам')
    parser.add_argument('-c', '--colors', nargs='+', required=True,
                       help='Список цветов для поиска')
    parser.add_argument('-t', '--total_count', type=int, required=True,
                       help='Общее количество изображений (50-1000)')
    parser.add_argument('-o', '--output_dir', type=str, default='snake_images',
                       help='Папка для сохранения изображений')
    parser.add_argument('-a', '--annotation', type=str, default='annotation.csv',
                       help='Файл для аннотации (CSV)')
    return parser.parse_args()


def download_colored_snakes(colors: list[str], total_count: int, output_dir: str) -> None:
    """
    Скачивание изображений змей разных цветов в одну папку
    """

    if not 50 <= total_count <= 1000:
        raise ValueError("Общее количество должно быть от 50 до 1000")
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Папка создана: {os.path.abspath(output_dir)}")

    counts = [1] * len(colors)
    for _ in range(total_count - len(colors)):
        counts[random.randint(0, len(colors) - 1)] += 1

    print(f"Общее количество: {total_count}")
    print("Распределение по цветам:")
    for color, count in zip(colors, counts):
        print(f"  {color}: {count}")
    
    time.sleep(5)


    for color, count in zip(colors, counts):
        
        color_dir = os.path.join(output_dir, color)
        os.makedirs(color_dir, exist_ok=True)
        
        print(f"Скачиваем {count} изображений цвета '{color}' в папку '{color_dir}'...")
        
        crawler = BingImageCrawler(storage={'root_dir': color_dir})
        crawler.crawl(keyword=f"snake {color}", max_num=count)


def create_annotation(output_dir: str, annotation_file: str) -> None:
    """
    Создание CSV файла с аннотацией путей к изображениям
    """

    image_paths = []
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                abs_path = os.path.abspath(os.path.join(root, file))
                rel_path = os.path.relpath(os.path.join(root, file))
                image_paths.append([abs_path, rel_path])
    
    data = [["Абсолютный путь", "Относительный путь"]] + image_paths
    
    with open(annotation_file, "w", newline="", encoding="utf-8-sig") as file:
        csv.writer(file).writerows(data)
    
    print(f"Создан файл аннотации: {annotation_file} ({len(image_paths)} записей)")


class ImageIterator:
    """
    Итератор по путям к файлам из CSV аннотации
    """
    
    def __init__(self, annotation_file: str):
        self.annotation_file = annotation_file
        self.data = []
        self.index = 0

    def __iter__(self):
        if os.path.exists(self.annotation_file):
            with open(self.annotation_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)
                self.data = [row for row in reader]
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


def main() -> None:
    args = parse_arguments()
    
    try:
        download_colored_snakes(args.colors, args.total_count, args.output_dir)
        create_annotation(args.output_dir, args.annotation)

        print("\nДемонстрация итератора:")
        iterator = ImageIterator(args.annotation)
        
        for i, (abs_path, rel_path) in enumerate(iterator):
            print(f"  {i+1}. {os.path.basename(rel_path)}")
            
        print("Готово! Все изображения скачаны.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()