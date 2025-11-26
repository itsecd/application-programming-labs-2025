import time
import os
import csv
from pathlib import Path
import threading
from icrawler.builtin import BingImageCrawler

class ImagePathIterator:
    """
    Итератор по путям к файлам изображений.
    Может работать как с файлом-аннотацией, так и с папкой напрямую.
    """
    
    def __init__(self, annotation_file=None, folder_path=None):
        """
        Args:
            annotation_file (str): Путь к CSV файлу с аннотациями
            folder_path (str): Путь к папке с изображениями
        """
        if annotation_file and os.path.exists(annotation_file):
            self.mode = 'annotation'
            self.annotation_file = annotation_file
        elif folder_path and os.path.exists(folder_path):
            self.mode = 'folder'
            self.folder_path = folder_path
        else:
            raise ValueError("Необходимо указать либо файл аннотации, либо путь к папке")
        
        self.current_index = 0
        self.file_paths = []
        self._load_paths()
    
    def _load_paths(self):
        """Загружает пути к файлам в зависимости от режима"""
        if self.mode == 'annotation':
            self._load_from_annotation()
        else:
            self._load_from_folder()
    
    def _load_from_annotation(self):
        """Загружает пути из CSV файла аннотации"""
        try:
            with open(self.annotation_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.file_paths.append(row['absolute_path'])
        except Exception as e:
            print(f"Ошибка при чтении файла аннотации: {e}")
    
    def _load_from_folder(self):
        """Загружает пути из папки"""
        try:
            for file_path in Path(self.folder_path).iterdir():
                if file_path.is_file():
                    self.file_paths.append(str(file_path.absolute()))
        except Exception as e:
            print(f"Ошибка при чтении папки: {e}")
    
    def __iter__(self):
        """Возвращает сам объект как итератор"""
        self.current_index = 0
        return self
    
    def __next__(self):
        """Возвращает следующий путь к файлу"""
        if self.current_index < len(self.file_paths):
            path = self.file_paths[self.current_index]
            self.current_index += 1
            return path
        else:
            raise StopIteration
    
    def __len__(self):
        """Возвращает количество файлов"""
        return len(self.file_paths)
    
def create_annotation_csv(image_folder, output_csv="annotation.csv"):
    """
    Создает CSV аннотацию с абсолютными и относительными путями к файлам.
    
    Args:
        image_folder (str): Папка с изображениями
        output_csv (str): Имя выходного CSV файла
    
    Returns:
        str: Путь к созданному CSV файлу
    """
    image_folder_path = Path(image_folder)
    
    if not image_folder_path.exists():
        raise ValueError(f"Папка {image_folder} не существует")
    
    # Получаем абсолютный путь к родительской директории для относительных путей
    parent_dir = image_folder_path.parent.absolute()
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'absolute_path', 'relative_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for file_path in image_folder_path.iterdir():
            if file_path.is_file():
                absolute_path = file_path.absolute()
                relative_path = absolute_path.relative_to(parent_dir)
                
                writer.writerow({
                    'filename': file_path.name,
                    'absolute_path': str(absolute_path),
                    'relative_path': str(relative_path)
                })
    
    print(f"Аннотация создана: {output_csv}")
    return output_csv

def download_images_with_timing(keyword, output_dir, min_images=50, max_time=60):
    """
    Скачивает изображения по ключевому слову с ограничением по времени и минимальному количеству.
    
    Args:
        keyword (str): Ключевое слово для поиска
        output_dir (str): Папка для сохранения изображений
        min_images (int): Минимальное количество изображений (по умолчанию 50)
        max_time (int): Максимальное время скачивания в секундах (по умолчанию 60)
    
    Returns:
        tuple: (количество скачанных изображений, затраченное время в секундах)
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        raise OSError("Не удалось создать дирректорию")
    downloaded_count = [0]
    
    start_time = time.time()
    
    def crawler_task():
        """Задача для запуска в отдельном потоке"""
        try:
            crawler = BingImageCrawler(storage={'root_dir': output_dir})
            crawler.crawl(keyword=keyword, max_num=1000)
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
    
    # поток
    crawler_thread = threading.Thread(target=crawler_task)
    crawler_thread.daemon = True
    crawler_thread.start()
    
    print(f"Начало скачивания изображений по запросу '{keyword}'...")
    print(f"Ограничения: минимум {min_images} изображений или максимум {max_time} секунд")
    
    while crawler_thread.is_alive():
        try:
            current_count = len([f for f in os.listdir(output_dir) 
                               if os.path.isfile(os.path.join(output_dir, f))])
            downloaded_count[0] = current_count
        except OSError:
            current_count = 0
        
        elapsed_time = time.time() - start_time
        
        # Условия
        if current_count >= min_images:
            print(f"Достигнуто минимальное количество изображений: {current_count}")
            break
            
        if elapsed_time >= max_time:
            print(f"Достигнуто максимальное время: {elapsed_time:.2f} секунд")
            break
        
        time.sleep(0.5)
    
    total_time = time.time() - start_time
    final_count = downloaded_count[0]
    
    return final_count, total_time



def main() -> None:
    """Основная функция"""
    keyword = "pig"
    output_dir = "downloaded_images"
    min_images = 50
    max_time = 60 
    
    print("ПРОГРАММА ДЛЯ СКАЧИВАНИЯ ИЗОБРАЖЕНИЙ")    
    count, time_spent = download_images_with_timing(
        keyword=keyword,
        output_dir=output_dir,
        min_images=min_images,
        max_time=max_time
    )
    
    print("РЕЗУЛЬТАТЫ СКАЧИВАНИЯ:")
    print(f"Ключевое слово: '{keyword}'")
    print(f"Папка сохранения: '{output_dir}'")
    print(f"Скачано изображений: {count}")
    print(f"Затраченное время: {time_spent:.2f} секунд")
    
    # Условия
    if count >= min_images:
        print("Минимальное количество изображений достигнуто!")
    else:
        print(f"Минимальное количество ({min_images}) не достигнуто")
    
    # Создание аннотации CSV
    print("СОЗДАНИЕ АННОТАЦИИ CSV")
    try:
        annotation_file = create_annotation_csv(output_dir)
        print(f"Аннотация успешно создана: {annotation_file}")
        
    except Exception as e:
        print(f"Ошибка при создании аннотации: {e}")


if __name__ == "__main__":
    main()