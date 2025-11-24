import csv
import os
import time
import threading
from typing import Optional, List, Iterator
from icrawler.builtin import BingImageCrawler


class ImageIterator:
    def __init__(self, annotation_file: Optional[str] = None, folder_path: Optional[str] = None) -> None:
        self.paths: List[str] = []
        
        try:
            if annotation_file:
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if row:
                            self.paths.append(row[0])
            elif folder_path:
                for file in os.listdir(folder_path):
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        full_path = os.path.abspath(os.path.join(folder_path, file))
                        self.paths.append(full_path)
        except Exception as e:
            raise Exception(f"Ошибка при инициализации итератора: {e}")

    def __iter__(self) -> Iterator[str]:
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration


def download_images(output_dir: str, timeout: int = 60, min_images: int = 50) -> None:
   
    stop_download = False
    
    def download_worker():
        try:
            crawler = BingImageCrawler(storage={'root_dir': output_dir})
            crawler.crawl(keyword='pig', max_num=100)
        except Exception:
            pass
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        download_thread = threading.Thread(target=download_worker)
        download_thread.daemon = True
        download_thread.start()
        
        start_time = time.time()
        end_time = start_time + timeout
        
        while time.time() < end_time:
            current_count = len([f for f in os.listdir(output_dir) 
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
   
    try:
        with open(annotation_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Абсолютный путь', 'Относительный путь'])
            
            if not os.path.exists(output_dir):
                raise Exception(f"Папка {output_dir} не существует")
            
            images = [f for f in os.listdir(output_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            if not images:
                raise Exception("В папке нет изображений для аннотации")
            
            for file in images:
                abs_path = os.path.abspath(os.path.join(output_dir, file))
                rel_path = os.path.relpath(abs_path, start=os.getcwd())
                writer.writerow([abs_path, rel_path])
                
    except Exception as e:
        raise Exception(f"Ошибка при создании аннотации: {e}")
