import argparse
import csv
import os
import time
from typing import List, Iterator, Tuple

from icrawler.builtin import BingImageCrawler

class ImageDownloader:
    """Класс для скачивания изображений обезьян."""
    
    def __init__(self) -> None:
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif']
        self.keywords = [
            "monkey",
            "monkey animal",
            "wild monkey", 
            "monkey wildlife",
            "jungle monkey",
            "baby monkey",
            "monkey primate",
            "monkey face",
            "monkey sitting",
            "monkey tree"
        ]
    
    def download_images(self, num_images: int, output_dir: str) -> int:
        """
        Скачивает изображения обезьян с гарантией минимума.
        
        Args:
            num_images: Целевое количество изображений
            output_dir: Папка для сохранения
            
        Returns:
            Количество скачанных изображений
        """
        try:
            print(f"Начинаем скачивание {num_images} изображений обезьян...")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            total_downloaded = 0
            max_attempts = 10
            
            for attempt in range(max_attempts):
                if total_downloaded >= 50:  
                    break
                    
                keyword = self.keywords[attempt % len(self.keywords)]
                needed = 50 - total_downloaded
                
                print(f"Попытка {attempt + 1}: '{keyword}' (нужно {needed})")
                
                downloaded = self._try_download(keyword, needed, output_dir, total_downloaded)
                total_downloaded += downloaded
                
                if downloaded > 0:
                    print(f"   Успешно: +{downloaded} изображений")
                else:
                    print("   Не удалось скачать")
                
                time.sleep(1)  # Пауза между запросами
            
            print(f"Итого скачано: {total_downloaded} изображений")
            return total_downloaded
            
        except Exception as e:
            print(f"Ошибка при скачивании изображений: {e}")
            return self._count_images(output_dir)
    
    def _try_download(self, keyword: str, max_num: int, output_dir: str, offset: int) -> int:
        """
        Попытка скачать изображения с обработкой ошибок.
        
        Args:
            keyword: Ключевое слово
            max_num: Максимальное количество
            output_dir: Папка для сохранения
            offset: Смещение для нумерации файлов
            
        Returns:
            Количество новых скачанных изображений
        """
        try:
            before_count = self._count_images(output_dir)
            
            crawler = BingImageCrawler(
                storage={'root_dir': output_dir},
                downloader_threads=1  
            )
            crawler.crawl(
                keyword=keyword,
                max_num=max_num,
                file_idx_offset=offset
            )
            
            after_count = self._count_images(output_dir)
            return after_count - before_count
            
        except Exception:
            return 0
    
    def _count_images(self, directory: str) -> int:
        """
        Подсчитывает количество изображений в директории.
    
        """
        try:
            images = [
                f for f in os.listdir(directory) 
                if any(f.lower().endswith(ext) for ext in self.supported_formats)
            ]
            return len(images)
        except OSError:
            return 0


class AnnotationManager:
    """Класс для создания и управления CSV аннотациями."""
    
    def create_annotation(self, images_dir: str, annotation_file: str) -> int:
        """
        Создает CSV файл с путями к изображениям.
        
        Args:
            images_dir: Папка с изображениями
            annotation_file: Путь к файлу аннотации
            
        Returns:
            Количество записанных строк
        """
        try:
            print(f"Создаем аннотацию {annotation_file}...")
            
            image_paths = self._get_image_paths(images_dir)
            
            with open(annotation_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['absolute_path', 'relative_path'])
                writer.writerows(image_paths)
            
            print(f"Записано {len(image_paths)} строк в аннотацию")
            return len(image_paths)
            
        except Exception as e:
            print(f"Ошибка при создании аннотации: {e}")
            return 0
    
    def _get_image_paths(self, directory: str) -> List[Tuple[str, str]]:
        """
        Получает абсолютные и относительные пути к изображениям.
        
        Args:
            directory: Папка с изображениями
            
        Returns:
            Список кортежей (абсолютный_путь, относительный_путь)
        """
        image_paths: List[Tuple[str, str]] = []
        
        if not os.path.exists(directory):
            return image_paths
        
        try:
            for filename in os.listdir(directory):
                if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    abs_path = os.path.abspath(os.path.join(directory, filename))
                    rel_path = os.path.join(directory, filename)
                    image_paths.append((abs_path, rel_path))
                    
        except OSError as e:
            print(f"Ошибка при чтении директории: {e}")
        
        return image_paths


class ImageIterator:
    """
    Итератор для перебора путей к изображениям из CSV файла или папки.
    """
    
    def __init__(self, annotation_file: str = None, folder_path: str = None) -> None:
        """
        Инициализация итератора.
        
        Args:
            annotation_file: Путь к CSV файлу с аннотациями
            folder_path: Путь к папке с изображениями
        """
        self.paths: List[str] = []
        self.index: int = 0
        
        if annotation_file and os.path.exists(annotation_file):
            self._load_from_annotation(annotation_file)
        elif folder_path and os.path.exists(folder_path):
            self._load_from_folder(folder_path)
        else:
            print("Предупреждение: не указан корректный файл аннотации или папка")
    
    def _load_from_annotation(self, annotation_file: str) -> None:
        """
        Загружает пути из CSV файла аннотации.
        
        Args:
            annotation_file: Путь к CSV файлу
        """
        try:
            with open(annotation_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'absolute_path' in row and os.path.exists(row['absolute_path']):
                        self.paths.append(row['absolute_path'])
            
            print(f"Загружено {len(self.paths)} путей из аннотации")
            
        except Exception as e:
            print(f"Ошибка при чтении аннотации: {e}")
    
    def _load_from_folder(self, folder_path: str) -> None:
        """
        Загружает пути из папки с изображениями.
        
        Args:
            folder_path: Путь к папке с изображениями
        """
        try:
            for filename in os.listdir(folder_path):
                if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    full_path = os.path.abspath(os.path.join(folder_path, filename))
                    if os.path.exists(full_path):
                        self.paths.append(full_path)
            
            print(f"Загружено {len(self.paths)} путей из папки")
            
        except OSError as e:
            print(f"Ошибка при чтении папки: {e}")
    
    def __iter__(self) -> Iterator[str]:
        """
        Возвращает итератор.
        
        Returns:
            self
        """
        self.index = 0
        return self
    
    def __next__(self) -> str:
        """
        Возвращает следующий путь к изображению.
        
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration
    
    def __len__(self) -> int:
        """
        Возвращает количество путей.

        """
        return len(self.paths)


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        Объект с аргументами
    """
    parser = argparse.ArgumentParser(
        description='Скачивание изображений обезьян и создание аннотации'
    )
    parser.add_argument(
        '--folder', 
        type=str, 
        required=True,
        help='Путь к папке для сохранения изображений'
    )
    parser.add_argument(
        '--annotation', 
        type=str, 
        required=True,
        help='Путь к файлу аннотации CSV'
    )
    
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_arguments()
        NUM_IMAGES = 50

        downloader = ImageDownloader()
        downloaded_count = downloader.download_images(NUM_IMAGES, args.folder)

        annotation_manager = AnnotationManager()
        annotation_count = annotation_manager.create_annotation(args.folder, args.annotation)
        
        print("\nТестируем итератор:")
        iterator = ImageIterator(annotation_file=args.annotation)
        
        print(f"Всего путей в итераторе: {len(iterator)}")
        
        if len(iterator) > 0:
            print("Первые 5 файлов:")
            count = 0
            for path in iterator:
                print(f"  {os.path.basename(path)}")
                count += 1
                if count >= 5:
                    break
        else:
            print("Нет изображений для отображения")
        
        print(f"\nОТЧЕТ:")
        print(f"Скачано изображений: {downloaded_count}")
        print(f"Записано в аннотацию: {annotation_count}")
        
        if downloaded_count >= 50:
            print("УСПЕХ: Достигнут минимум 50 изображений!")
        else:
            print(f" Предупреждение: скачано только {downloaded_count} изображений")
        
        print("Работа завершена!")
        
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == '__main__':
    main()