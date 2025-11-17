import os
import random
import time
from datetime import datetime

from icrawler.builtin import BingImageCrawler


class ImageDownloader:
    """
    Класс для скачивания изображений обезьян из интернета.
    Автоматически определяет текущий год и ищет актуальные изображения.
    """

    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif']

        # Ключевые слова для поиска изображений обезьян
        self.keywords = [
            "monkey", "monkey animal", "monkey wildlife",
            "baboon", "orangutan", "chimpanzee"
        ]

        # Автоматически определяем текущий год
        self.current_year = datetime.now().year

    def download_images(self, num_images, output_dir):
        """
        Основной метод для скачивания изображений.

        Args:
            num_images: количество изображений для скачивания
            output_dir: папка для сохранения изображений
        """
        print(f"Скачиваем {num_images} изображений обезьян за {self.current_year} год...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Очищаем папку от старых файлов перед началом скачивания
        self.clean_directory(output_dir)

        total_downloaded = 0
        max_attempts = 10

        for attempt in range(max_attempts):
            if total_downloaded >= num_images:
                break

            # Выбираем случайное ключевое слово
            keyword = random.choice(self.keywords)
            needed = num_images - total_downloaded

            print(f"Попытка {attempt + 1}: поиск '{keyword}'")

            downloaded = self.try_download(keyword, needed, output_dir, total_downloaded)
            total_downloaded += downloaded

            if downloaded > 0:
                print(f"Скачано: {downloaded} изображений")

            time.sleep(1)

        print(f"Всего скачано: {total_downloaded} изображений")
        return total_downloaded

    def try_download(self, keyword, max_num, output_dir, offset):
        """
        Пытается скачать изображения с определенным ключевым словом.

        Args:
            keyword: ключевое слово для поиска
            max_num: максимальное количество для скачивания
            output_dir: папка для сохранения
            offset: смещение для нумерации файлов
        """
        try:
            before_count = self.count_images(output_dir)

            date_filters = [
                f"after:{self.current_year}-01-01",  # С начала года
                f"after:{self.current_year}-03-01",
                ""  # Без фильтра даты
            ]

            date_filter = random.choice(date_filters)
            search_query = f"{keyword} {date_filter}".strip()

            print(f"Запрос: '{search_query}'")

            crawler = BingImageCrawler(storage={'root_dir': output_dir})

            crawler.crawl(
                keyword=search_query,
                max_num=max_num,
                file_idx_offset=offset
            )

            # Считаем сколько изображений стало после скачивания
            after_count = self.count_images(output_dir)
            return after_count - before_count

        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
            return 0

    def clean_directory(self, directory):
        """
        Очищает папку от всех файлов перед началом скачивания.
        Это нужно чтобы удалить старые изображения.
        """
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)  # Удаляем файл
                except Exception as e:
                    print(f"Ошибка удаления {file_path}: {e}")

    def count_images(self, directory):
        """
        Подсчитывает количество изображений в папке.

        Returns:
            Количество файлов с поддерживаемыми форматами
        """
        try:
            images = [
                f for f in os.listdir(directory)
                if any(f.lower().endswith(ext) for ext in self.supported_formats)
            ]
            return len(images)
        except OSError:
            return 0