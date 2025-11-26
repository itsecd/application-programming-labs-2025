from icrawler.builtin import GoogleImageCrawler
import time
import os
import signal

keyword = "pig"
min_images = 50
time_limit = 30  # в секундах
root_dir = "pig_images"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# Глобальная переменная для отслеживания времени
start_time = None
crawler = None

class TimedCrawler:
    def __init__(self, time_limit, min_images):
        self.time_limit = time_limit
        self.min_images = min_images
        self.start_time = None
        self.should_stop = False
        self.downloaded_count = 0
        
    def timeout_handler(self, signum, frame):
        """Обработчик сигнала таймера"""
        print("\nДостигнут лимит времени - останавливаем скачивание...")
        self.should_stop = True
        if crawler:
            crawler.feeder.stop()
            crawler.parser.stop()
            crawler.downloader.stop()
    
    def file_downloaded_callback(self, img, task):
        """Callback-функция, вызываемая после каждого скачанного файла"""
        self.downloaded_count += 1
        elapsed_time = time.time() - self.start_time
        
        print(f"Скачано: {self.downloaded_count} изображений, "
              f"время: {elapsed_time:.1f}с")
        
        # Проверяем условия остановки
        if (elapsed_time >= self.time_limit or 
            self.downloaded_count >= self.min_images):
            print("Условие достигнуто - останавливаем скачивание...")
            self.should_stop = True
            if crawler:
                crawler.feeder.stop()
                crawler.parser.stop()
                crawler.downloader.stop()
        
        return not self.should_stop

def count_downloaded_images():
    """Подсчитывает количество скачанных изображений"""
    try:
        return len([f for f in os.listdir(root_dir) 
                  if os.path.isfile(os.path.join(root_dir, f))])
    except FileNotFoundError:
        return 0