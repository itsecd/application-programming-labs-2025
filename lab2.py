from icrawler.builtin import GoogleImageCrawler
import threading
import time
import os
import signal

keyword = "pig"
min_images = 50
time_limit = 30
root_dir = "pig_images"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# Глобальные переменные для управления потоком
downloader_thread = None
crawler = None

def run_crawler():
    """
    Функция для запуска краулера в отдельном потоке
    """
    global crawler
    crawler = GoogleImageCrawler(
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=4,
        storage={'root_dir': root_dir}
    )
    crawler.crawl(
        keyword=keyword,
        max_num=1000
    )

def stop_crawler():
    """Функция для принудительной остановки краулера"""
    if crawler:
        # Останавливаем все компоненты краулера
        crawler.feeder.stop()
        crawler.parser.stop()
        crawler.downloader.stop()