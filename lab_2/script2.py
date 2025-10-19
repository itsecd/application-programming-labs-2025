import argparse
import csv
import os
import time
from pathlib import Path

from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
from PIL import Image


class ImagePathIterator:
    """Итератор по путям к изображениям"""

    def __init__(self, source):
        """Инициализация итератора по CSV или папке"""
        self.paths = []

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

        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration

    def __len__(self):
        return len(self.paths)



def download_images(keyword, num_images, min_size, max_size, save_dir):
    """Загружает изображения с Baidu, Bing, Google. Останавливается при достижении нужного количества"""
    os.makedirs(save_dir, exist_ok=True)
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    def get_current_count():
        return len([
            f for f in os.listdir(save_dir)
            if Path(f).suffix.lower() in image_extensions
        ])

    need_count = num_images
    sources = [
        ("Baidu", BaiduImageCrawler),
        ("Bing", BingImageCrawler),
        ("Google", GoogleImageCrawler)
    ]

    for source_name, crawler_class in sources:
        current_count = get_current_count()
        if current_count >= need_count:
            print(f"\nДостигнуто {current_count} изображений, загрузка завершена")
            break

        remaining = need_count - current_count
        download_count = min(remaining * 3, 1000)

        print(f"\nИсточник: {source_name}, необходимо ещё {remaining} изображений")

        crawler = crawler_class(
            storage={'root_dir': save_dir},
            downloader_threads=2,
            parser_threads=1,
            feeder_threads=1
        )

        before = get_current_count()
        try:
            crawler.crawl(keyword=keyword, max_num=download_count)
        except Exception as e:
            print(f"Ошибка при работе с {source_name}: {e}")

        time.sleep(2)
        after = get_current_count()
        new_files = after - before

        print(f"Загружено с {source_name}: {new_files}, всего: {after}")

        if after >= need_count:
            print(f"Достигнута цель: {after} изображений")
            break

    total_downloaded = get_current_count()
    if total_downloaded < need_count:
        print(f"\nУдалось скачать только {total_downloaded} из {need_count}")

    print(f"\nФильтрация по размеру: от {min_size} до {max_size}")
    remaining = filter_images_by_size(save_dir, min_size, max_size)
    print(f"Осталось изображений после фильтрации: {remaining}")

    if remaining < need_count:
        shortage = need_count - remaining
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

    final_count = get_current_count()
    if final_count > need_count:
        files = sorted([
            f for f in os.listdir(save_dir)
            if Path(f).suffix.lower() in image_extensions
        ])
        for f in files[need_count:]:
            os.remove(os.path.join(save_dir, f))
        print(f"Удалено лишние файлы, оставлено {need_count}")

    final_count = get_current_count()
    print(f"\nИтого: {final_count} файлов сохранено в {save_dir}")




