import csv #чтения и записи табличных данных в текстовом формате
import os  #для работы с файловой системой
import time
import threading #для работы с многопоточностью
from typing import Optional, List, Iterator
from icrawler.builtin import BingImageCrawler


class ImageIterator:
    """Итератор для работы с путями к изображениям."""
    
    def __init__(self, annotation_file: Optional[str] = None, folder_path: Optional[str] = None) -> None:
        """Инициализирует итератор изображений.
        
        Args:
            annotation_file: Путь к CSV-файлу с аннотацией изображений.
            folder_path: Путь к папке с изображениями.
        """
        self.paths: List[str] = [] #сохр все пути к изображ
        
        try:
            if annotation_file:
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f) # созд объект, построчно читать 
                    next(reader)
                    for row in reader:
                        if row:
                            self.paths.append(row[0])
            elif folder_path:
                for file in os.listdir(folder_path): #получ список всех файлов и перебирает в цикле
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.abspath(os.path.join(folder_path, file))# путь к папке и имя в абсолют путь
                        self.paths.append(full_path)
        except Exception as e:
            raise Exception(f"Ошибка при инициализации итератора: {e}")

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор для объекта."""
        self.index = 0
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к изображению.
        
        Raises:
            StopIteration: Когда все пути пройдены.
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


def download_images(output_dir: str, timeout: int = 60, min_images: int = 50) -> None:
    """Скачивает изображения свиней с помощью Bing Image Crawler.
    
    Args:
        output_dir: Папка для сохранения изображений.
        timeout: Максимальное время скачивания в секундах.
        min_images: Минимальное количество изображений для скачивания.
        
    Raises:
        Exception: Если не удалось скачать ни одного изображения.
    """
    stop_download = False
    
    def download_worker():
        """Рабочая функция для потока скачивания."""
        try:
            crawler = BingImageCrawler(storage={'root_dir': output_dir}) #создает объект для скачивания
            crawler.crawl(keyword='pig', max_num=100) #процесс скачивания 
        except Exception:
            pass
    
    try:
        os.makedirs(output_dir, exist_ok=True) #Создаёт папку для изображений
        
        download_thread = threading.Thread(target=download_worker) #Создаёт новый поток выполнения
        download_thread.daemon = True
        download_thread.start()
        
        start_time = time.time()
        end_time = start_time + timeout
        
        while time.time() < end_time:
            current_count = len([f for f in os.listdir(output_dir)  #количество изображений в папке
                               if f.endswith(('.jpg', '.jpeg', '.png'))])
            
            if current_count >= min_images:
                break
                
            time.sleep(1)
        
        stop_download = True
        
        final_count = len([f for f in os.listdir(output_dir) 
                          if f.endswith(('.jpg', '.jpeg', '.png'))])
        
        if final_count == 0:
            raise Exception("Не удалось скачать ни одного изображения")
                
    except Exception as e:
        raise Exception(f"Ошибка при скачивании изображений: {e}")


def create_annotation(annotation_file: str, output_dir: str) -> None:
    """Создает CSV-файл аннотации с путями к изображениям.
    
    Args:
        annotation_file: Имя файла для аннотации.
        output_dir: Папка с изображениями.
        
    Raises:
        Exception: Если папка не существует или в ней нет изображений.
    """
    try:
        with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f) #Создаёт объект для записи данных в CSV-формат
            writer.writerow(['Абсолютный путь', 'Относительный путь'])
            
            if not os.path.exists(output_dir):
                raise Exception(f"Папка {output_dir} не существует")
            
            #Создает список всех файлов изображений в папке
            images = [f for f in os.listdir(output_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            if not images:
                raise Exception("В папке нет изображений для аннотации")
            
            for file in images:
                abs_path = os.path.abspath(os.path.join(output_dir, file)) #Создает абсолютный путь к изображению
                rel_path = os.path.relpath(abs_path, start=os.getcwd())
                writer.writerow([abs_path, rel_path])
                
    except Exception as e:
        raise Exception(f"Ошибка при создании аннотации: {e}")
