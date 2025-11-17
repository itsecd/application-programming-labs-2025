import csv
import os
import argparse
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
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        print(f"Скачивание изображений в директорию: {save_dir}")
        
        global_downloaded_images = 0

        for keyword in self.keywords:
            images_num = random.randint(10, 50)

            print(f"Скачивание {images_num} изображений для ключевого слова: '{keyword}'")

            keyword_dir = os.path.join(save_dir, keyword.replace(' ', '_'))
            if not os.path.exists(keyword_dir):
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

class ImagePathIterator:
    """Итератор путей файлов"""
    def __init__(self, annotation_path: str) -> None:
        """
        Args:
            annotation_path: Путь к файлу с аннотацией
        """
        if isinstance(annotation_path, str):
            if annotation_path.endswith('.csv'):
                self.annotation_file=annotation_path
                self.use_annotation=True
            else:
                self.folder_path=annotation_path
                self.use_annotation=False
        else:
            raise ValueError("Annotation_path must be a string")

        self.current_index=0
        self.image_paths=[]
        self._load_paths()

    def _load_paths(self) -> None:
        """Загружает пути к изображениям из файла с аннотацией или папки"""
        if self.use_annotation:
            try:
                with open(self.annotation_file, 'r', encoding='utf-8') as csvfile:
                    reader=csv.DictReader(csvfile)
                    for row in reader:
                        file_path = row['Absolute path']
                        if os.path.exists(file_path):
                            self.image_paths.append(file_path)
            except FileNotFoundError:
                return
        else:
            if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
                image_extensions=['.jpg','.jpeg','.png','.gif','.bmp']
                for root, dirs, files in os.walk(self.folder_path):
                    for file in files:
                        file_path=os.path.join(root, file)
                        if os.path.isfile(file_path):
                            _, file_extension = os.path.splitext(file)
                            file_ext=file_extension.lower()

                            if file_ext in image_extensions:
                                abs_path = os.path.abspath(file_path)
                                self.image_paths.append(abs_path)
                

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор."""
        self.current_index = 0
        return self

    
    def __next__(self) -> str:
        """Возвращает следующий путь к изображению."""
        if self.current_index < len(self.image_paths):
            path = self.image_paths[self.current_index]
            self.current_index += 1
            return path
        else:
            raise StopIteration


    def __len__(self) -> int:
        """Возвращает количество путей"""
        return len(self.image_paths)
    

def main() -> None:
    parser = argparse.ArgumentParser(description='Скачивание изображений по ключевым словам')
    parser.add_argument('--keywords', '-k', nargs='+', required=True, help='Ключевые слова для поиска изображений')
    parser.add_argument('--save_dir', '-s', required=True, help='Путь к папке для сохранения изображений')
    parser.add_argument('--annotation_file', '-a', required=True, help='Путь к файлу с аннотацией')

    args = parser.parse_args()
    
    print("=" * 50)
    print("ЗАПУСК СКАЧИВАНИЯ ИЗОБРАЖЕНИЙ")
    print("=" * 50)
    print(f"Ключевые слова: {', '.join(args.keywords)}")
    print(f"Директория сохранения: {args.save_dir}")
    print(f"Файл аннотации: {args.annotation_file}")
    print(f"Диапазон изображений на слово: 1-50 (фиксировано)")
    print("=" * 50)
    
    downloader = ImageDownloader(keywords=args.keywords)
    
    total_downloaded = downloader.download_images(args.save_dir)
    downloader.create_annotation(args.save_dir, args.annotation_file)
    
    print("\n" + "=" * 30)
    print("ДЕМОНСТРАЦИЯ ИТЕРАТОРА")
    print("=" * 30)
    
    iterator = ImagePathIterator(args.annotation_file)
    
    print(f"Всего файлов в аннотации: {len(iterator)}")
    
    if len(iterator) > 0:
        print("Первые 5 файлов:")
        for i, path in enumerate(iterator):
            if i < 5:
                filename = os.path.basename(path)
                print(f"{i + 1}. {filename}")
    else:
        print("Файлы не найдены")
    
    print("=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНA")
    print("=" * 50)


if __name__ == "__main__":
    main()

            