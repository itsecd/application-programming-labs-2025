import argparse
import csv
import os
import random
from typing import List, Iterator
from icrawler.builtin import BingImageCrawler


class ImageDownloader:
    """Класс для скачивания изображений по ключевым словам"""
    def __init__(self, keywords: List[str]) -> None:
        """
        Args:
            keywords: Список ключевых слов    
        """
        self.keywords = keywords

    def download_images(self, save_dir: str) -> int:
        """Скачивает изображения по ключевым словам

        Args:
            save_dir: Директория для сохранения изображений

        Returns:
            Количество скачанных изображений
        """
        
        os.makedirs(save_dir, exist_ok=True)

        print(f"Скачивание изображений в директорию: {save_dir}")
        
        global_downloaded_images = 0

        for keyword in self.keywords:
            images_num = random.randint(10, 50)

            print(f"Скачивание {images_num} изображений для ключевого слова: '{keyword}'")

            keyword_dir = os.path.join(save_dir, keyword.replace(' ', '_'))
        
            os.makedirs(keyword_dir, exist_ok=True)

            crawler = BingImageCrawler(
                storage={'root_dir': keyword_dir},
                downloader_threads=1,
                parser_threads=1,
                feeder_threads=1
            )

            try:
                crawler.crawl(keyword=keyword, max_num=images_num)

                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
                downloaded_count = 0

                for filename in os.listdir(keyword_dir):
                    file_path = os.path.join(keyword_dir, filename)
                    if os.path.isfile(file_path):
                        _, file_extension = os.path.splitext(filename)
                        file_ext = file_extension.lower()

                        if file_ext in image_extensions:
                            global_downloaded_images += 1
                            downloaded_count += 1

                print(f"Успешно скачано {downloaded_count} изображений для '{keyword}'")

            except Exception as e:
                print(f"Ошибка при скачивании изображений по ключевому слову '{keyword}': {e}")
                continue

        print(f"Скачивание завершено. Всего скачано изображений: {global_downloaded_images}")
        return global_downloaded_images

    def create_annotation(self, save_dir: str, annotation_file: str) -> None:
        """Создает файл аннотации скачанных изображений

        Args:
            save_dir: Директория с изображениями
            annotation_file: Файл для записи аннотации
        """
        with open(annotation_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Absolute path', 'Relative path', 'Keyword'])

            for keyword in self.keywords:
                keyword_dir = os.path.join(save_dir, keyword.replace(' ', '_'))
                if not os.path.exists(keyword_dir):
                    continue

                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
                
                for filename in os.listdir(keyword_dir):
                    file_path = os.path.join(keyword_dir, filename)
                    if os.path.isfile(file_path):
                        _, file_extension = os.path.splitext(filename)
                        file_ext = file_extension.lower()

                        if file_ext in image_extensions:
                            abs_path = os.path.abspath(file_path)
                            rel_path = os.path.relpath(file_path)
                            writer.writerow([abs_path, rel_path, keyword])