import argparse
import csv
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Iterator, Optional, Union

from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
from PIL import Image


class ImagePathIterator:
    """Итератор по путям к изображениям"""

    def __init__(self, source: str) -> None:
        """Инициализация итератора по CSV или папке"""
        self.paths: List[str] = []

        if os.path.isfile(source) and source.endswith('.csv'):
            with open(source, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.paths = [row['absolute_path'] for row in reader]
        elif os.path.isdir(source):
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            self.paths = [
                str(Path(source) / f)
                for f in os.listdir(source)
                if Path(f).suffix.lower() in image_extensions
            ]
        else:
            raise ValueError("Источник должен быть CSV-файлом или папкой")

        self.index: int = 0

    def __iter__(self) -> Iterator[str]:
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self.paths)


def filter_images_by_size(image_dir: str, min_size: Tuple[int, int], max_size: Tuple[int, int]) -> int:
    """Удаляет изображения, не соответствующие диапазону размеров"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    removed_count: int = 0
    kept_count: int = 0

    time.sleep(1)

    files_to_process: List[str] = [
        f for f in os.listdir(image_dir)
        if Path(f).suffix.lower() in image_extensions
    ]

    print(f"\nПроверка {len(files_to_process)} изображений...")

    for filename in files_to_process:
        filepath = os.path.join(image_dir, filename)
        try:
            with Image.open(filepath) as img:
                width, height = img.size

            if (width < min_size[0] or height < min_size[1] or
                    width > max_size[0] or height > max_size[1]):
                os.remove(filepath)
                removed_count += 1
            else:
                kept_count += 1
        except Exception:
            try:
                os.remove(filepath)
                removed_count += 1
            except Exception:
                pass

    print(f"Фильтрация завершена: оставлено {kept_count}, удалено {removed_count}")
    return kept_count


def download_images(keyword: str, num_images: int, min_size: Tuple[int, int], 
                   max_size: Tuple[int, int], save_dir: str) -> None:
    """Загружает изображения с Baidu, Bing, Google. Останавливается при достижении нужного количества"""
    os.makedirs(save_dir, exist_ok=True)
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    def get_current_count() -> int:
        return len([
            f for f in os.listdir(save_dir)
            if Path(f).suffix.lower() in image_extensions
        ])

    need_count: int = num_images
    sources: List[Tuple[str, Any]] = [
        ("Baidu", BaiduImageCrawler),
        ("Bing", BingImageCrawler),
        ("Google", GoogleImageCrawler)
    ]

    for source_name, crawler_class in sources:
        current_count: int = get_current_count()
        if current_count >= need_count:
            print(f"\nДостигнуто {current_count} изображений, загрузка завершена")
            break

        remaining: int = need_count - current_count
        download_count: int = min(remaining * 3, 1000)

        print(f"\nИсточник: {source_name}, необходимо ещё {remaining} изображений")

        crawler = crawler_class(
            storage={'root_dir': save_dir},
            downloader_threads=2,
            parser_threads=1,
            feeder_threads=1
        )

        before: int = get_current_count()
        try:
            crawler.crawl(keyword=keyword, max_num=download_count)
        except Exception as e:
            print(f"Ошибка при работе с {source_name}: {e}")

        time.sleep(2)
        after: int = get_current_count()
        new_files: int = after - before

        print(f"Загружено с {source_name}: {new_files}, всего: {after}")
        if after >= need_count:
            print(f"Достигнута цель: {after} изображений")
            break

    total_downloaded: int = get_current_count()
    if total_downloaded < need_count:
        print(f"\nУдалось скачать только {total_downloaded} из {need_count}")

    print(f"\nФильтрация по размеру: от {min_size} до {max_size}")
    remaining: int = filter_images_by_size(save_dir, min_size, max_size)
    print(f"Осталось изображений после фильтрации: {remaining}")

    while remaining < need_count:
        shortage: int = need_count - remaining
        print(f"\nНедостача после фильтрации: {shortage} изображений")

        for source_name, crawler_class in sources:
            if get_current_count() >= need_count:
                break

            print(f"\nДокачка через {source_name}")
            crawler = crawler_class(storage={'root_dir': save_dir})

            try:
                crawler.crawl(keyword=keyword, max_num=shortage * 2)
            except Exception as e:
                print(f"Ошибка: {e}")

            time.sleep(2)
            remaining = filter_images_by_size(save_dir, min_size, max_size)
            print(f"Теперь доступно: {remaining}")

    final_count: int = get_current_count()
    if final_count > need_count:
        files: List[str] = sorted([
            f for f in os.listdir(save_dir)
            if Path(f).suffix.lower() in image_extensions
        ])
        for f in files[need_count:]:
            os.remove(os.path.join(save_dir, f))
        print(f"Удалено лишние файлы, оставлено {need_count}")

    final_count = get_current_count()
    print(f"\nИтого: {final_count} файлов сохранено в {save_dir}")


def create_annotation_csv(image_dir: str, csv_path: str) -> int:
    """Создаёт CSV с метаданными изображений"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_dir_path: Path = Path(image_dir).resolve()
    files_info: List[Dict[str, Any]] = []

    for filename in sorted(os.listdir(image_dir)):
        if Path(filename).suffix.lower() in image_extensions:
            abs_path: str = str(image_dir_path / filename)
            rel_path: str = os.path.relpath(abs_path, start=os.getcwd())

            files_info.append({
                'filename': filename,
                'absolute_path': abs_path,
                'relative_path': rel_path
            })

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames: List[str] = ['filename', 'absolute_path', 'relative_path']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(files_info)

    return len(files_info)


def main() -> None:
    """Точка входа команды. Управляет загрузкой и аннотацией"""
    parser = argparse.ArgumentParser(description='Скачивание изображений через icrawler')
    parser.add_argument('--keyword', type=str, default='cat', help='Ключевое слово поиска')
    parser.add_argument('--num_images', type=int, default=50, help='Количество изображений (50-1000)')
    parser.add_argument('--min_size', type=int, nargs=2, default=[200, 200], metavar=('W', 'H'))
    parser.add_argument('--max_size', type=int, nargs=2, default=[5000, 5000], metavar=('W', 'H'))
    parser.add_argument('--save_dir', type=str, default='./images', help='Папка для сохранения')
    parser.add_argument('--csv_path', type=str, default='./annotation.csv', help='CSV файл аннотации')
    args: argparse.Namespace = parser.parse_args()

    if not (50 <= args.num_images <= 1000):
        print("Ошибка: количество изображений должно быть от 50 до 1000")
        return

    download_images(args.keyword, args.num_images, tuple(args.min_size), tuple(args.max_size), args.save_dir)
    total_files: int = create_annotation_csv(args.save_dir, args.csv_path)

    if total_files == 0:
        print("\nНе удалось скачать изображения. Попробуйте изменить параметры.")
        return

    print("\nДемонстрация итератора")
    iterator_csv: ImagePathIterator = ImagePathIterator(args.csv_path)
    print(f"Из CSV: {len(iterator_csv)} файлов, первые 5:")
    for i, path in enumerate(iterator_csv):
        if i >= 5:
            break
        print(f"{i + 1}. {Path(path).name}")

    iterator_dir: ImagePathIterator = ImagePathIterator(args.save_dir)
    print(f"\nИз каталога: {len(iterator_dir)} файлов, первые 3:")
    for i, path in enumerate(iterator_dir):
        if i >= 3:
            break
        print(f"{i + 1}. {Path(path).name}")

    print("\nЗавершено успешно.")


if __name__ == '__main__':
    main()