import argparse
import os
import sys
import csv

from icrawler.builtin import BingImageCrawler

from pathlib import Path
FILE = 'annotation.csv'

COLORS = ["red", "green", "blue", "yellow", "black", "white"]
IMAGE_EXT = {'.jpg', '.jpeg', '.png'}

def parse_args() -> argparse.Namespace:
    """Принимает цвет и кол-во PNG в виде аргумента."""
    parser = argparse.ArgumentParser(
        description="Скачивание изображений черепах заданных цветов с использованием icrawler. Пример: py Lab2_var6.py --colors red --num_images 50"
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        required=True,
        help=f"Цвета для поиска: {', '.join(COLORS)} Выберите один или несколько цветов через запятую (например: red,blue)",
    )
    parser.add_argument(
        "--num_images",
        type=int,
        required=True,
        help="Общее количество изображений для скачивания (от 50 до 1000).",
    )
    return parser.parse_args()


def valid_colors(colors: list[str]) -> list[str]:
    """Приведения текста в нижний регистр"""
    valid_colors = []
    invalid_colors = []
    for color in colors:
        cleaned_color = color.strip().lower()
        if cleaned_color in COLORS:
            valid_colors.append(cleaned_color)
        else:
            invalid_colors.append(color)

    if invalid_colors:
        raise ValueError(
            f"Недопустимые цвета: {invalid_colors}. Допустимые: {(COLORS)}"
        )

    return valid_colors


def validate_total_images(total_images: int) -> None:
    """Проверка кол-ва фотографий"""
    if not (10 <= total_images <= 1000):
        raise ValueError("Количество изображений должно быть от 50 до 1000.")


def distribute_num_images(selected_colors: list[str], total_images: int) -> tuple[int,int]:
    """Распределяет общее кол-во PNG на каждый цвет"""
    num_colors = len(selected_colors)
    images_per_color = (
        total_images // num_colors
    )  # сколько достанеться фотографий каждому цвету
    remainder = (
        total_images % num_colors
    )  # остаток, который можно распределить дополнительно
    return images_per_color, remainder


def create_dir():
    """Создание папки turtle"""
    base_dir = "turtle_images"
    os.makedirs(
        base_dir, exist_ok=True
    )  # exist_ok=True - если папка существует, ничего не делать, ошибки не будет
    return base_dir


def search_download(selected_colors: list[str], images_per_color: int, remainder:int, base_dir: str):
    """Скачивание PNG под каждый цвет"""
    for i, color in enumerate(
        selected_colors
    ):  # enumerate позволяет одновременно получать индекс i и значение color элемента
        count = images_per_color + (1 if i < remainder else 0) #тернарный опер.
        search_keyword = f"turtle {color}"
        print(f"Скачивание {count} изображений по запросу: '{search_keyword}'")

        crawler = BingImageCrawler(
            storage={"root_dir": os.path.join(base_dir, color)}
        )
        crawler.crawl(keyword=search_keyword, max_num=count)

    print(f"Загрузка завершена. Изображения сохранены в папку '{base_dir}'.")

def collect_image_paths(base_dir: str):
    """Собирает все .jpg/.jpeg/.png файлы в base_dir рекурсивно."""
    paths = []
    base_path = Path(base_dir).resolve() #resolve - абсолютный путь
    for file_path in base_path.rglob('*'):
        if file_path.suffix.lower() in IMAGE_EXT:
            relative = file_path.relative_to(Path.cwd()) #Path.cwd() — текущая рабочая директория (откуда запущен скрипт).
            absolute = file_path.resolve() #абс.путь до png
            paths.append((str(absolute), str(relative)))
    return paths

def write_annotation_csv(paths, csv_file = FILE):
    """Записывает абсолютные и относительные пути turtle_images в CSV."""
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['absolute_path', 'relative_path'])
        writer.writerows(paths)
    print(f"Аннотация сохранена в '{csv_file}'")

class ImageIterator:
    """
    Итератор по путям к изображениям.
    
    Параметры:
        source (str): путь к CSV-файлу аннотации ИЛИ к папке с изображениями.
    """
    def __init__(self, source: str):
        self.paths = []
        source_path = Path(source)

        if source_path.is_file() and source_path.suffix.lower() == '.csv':
            # Загружаем из CSV
            with open(source_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not {'absolute_path', 'relative_path'}.issubset(reader.fieldnames):
                    raise ValueError("CSV должен содержать колонки 'absolute_path' и 'relative_path'")
                self.paths = [row['absolute_path'] for row in reader]
        elif source_path.is_dir():
            # Сканируем папку
            for file in source_path.rglob('*'):
                if file.suffix.lower() in IMAGE_EXT:
                    self.paths.append(str(file.resolve()))
        else:
            raise ValueError(f"Источник '{source}' не является ни существующей папкой, ни CSV-файлом.")

        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.paths):
            path = self.paths[self._index]
            self._index += 1
            return path
        else:
            raise StopIteration

def main():
    args = parse_args()
    try:
        colors = args.colors
        total_images = args.num_images
        
        validate_total_images(total_images)
        selected_colors = valid_colors(colors)

        images_per_color, reminder = distribute_num_images(selected_colors, total_images)
        search_download(selected_colors, images_per_color, reminder, create_dir())
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    
    #csv
    write_annotation_csv(collect_image_paths(create_dir()))
    # итератор
    print("\n🔍 Пример: первые 3 пути через ImageIterator:")
    try:
        iter = ImageIterator(FILE)  # или ImageIterator('turtle_images')
        for i, path in enumerate(iter):
            if i >= 3:
                break
            print(f"  {i+1}. {path}")
    except Exception as e:
        print(f"⚠️ Ошибка при итерации: {e}")

if __name__ == "__main__":
    main()
