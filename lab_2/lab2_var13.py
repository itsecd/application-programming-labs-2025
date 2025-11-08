import os
import argparse
import csv
import random
from icrawler.builtin import icrawler


class imageDownloader:
    """Класс для скачивания изображений по ключевым словам"""
    def __init__(self, keywords):
        """
        Args:
            keywords: Список ключевых слов    
        """
        self.keywords = keywords

    def download_images(self, save_dir, annotation_file):
        """Скачивает изображения и создает аннотацию

        Args:
            save_dir: Директория для сохранения изображений
            annotation_file: Файл для записи аннотации
        """

        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        print(f"Скачивание изображений в директорию:{save_dir}")
        
        with open(annotation_file, 'w', encoding='utf-8') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(['Абсолютный путь','Относительный путь', 'Ключевое слово'])

            global_downloaded_images=0

            for keyword in self.keywords:
                images_num=random.randint(1, 50)

                print(f"Скачивание {images_num} изображений, в директорию: {save_dir}")

                keyword_dir = os.path.join(save_dir, keyword.replace(' ', '_'))
                if not os.path.exists(keyword_dir):
                    os.makedirs(keyword_dir, exist_ok=True)

                crawler = GoogleImageCrawler(storage={'root dir': keyword_dir})

                try:
                    crawler.crawl(keyword=keyword, max_num=images_num)

                    image_extensions=['.jpg','.jpeg','.png','.gif','.bmp']
                    downloaded_count=0

                    for filename in os.listdir(keyword_dir):
                        file_path=os.join(keyword_dir, filename)
                        if os.path.isfile(file_path):
                            _, file_extension=os.path.splitext(file_path)
                            file_ext=file_extension.lower

                            if file_ext in image_extensions:
                                abs_path=os.path.abspath(file_path)
                                parent_dir=os.path.dirname(save_dir)
                                rel_path=os.path.relpath(file_path, parent_dir)

                                writer.writerow([abs_path, rel_path, keyword])

                                global_downloaded_images+=1
                                downloaded_count+=1

                except Exception as e:
                    print(f"Ошибка при скачивании изображений по ключевому слову '{keyword}': {e}")
                    continue
