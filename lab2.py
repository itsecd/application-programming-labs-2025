import time
import os
import threading
from icrawler.builtin import BingImageCrawler


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
    print("\n")
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
    


if __name__ == "__main__":
    main()