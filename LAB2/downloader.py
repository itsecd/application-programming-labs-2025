import time
from pathlib import Path
from typing import List

try:
    from icrawler.builtin import GoogleImageCrawler
except ImportError:
    print("Ошибка: Не установлен icrawler. Установите: pip install icrawler")
    import sys
    sys.exit(1)


def download_images_simple(keywords: List[str], num_images_per_keyword: int, output_dir: str) -> List[Path]:
    """
    Упрощенная версия скачивания изображений
    """
    print(f"Скачивание {len(keywords) * num_images_per_keyword} изображений...")
    print(f"Ключевые слова: {', '.join(keywords)}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_downloaded_files: List[Path] = []
    
    for keyword in keywords:
        print(f"\n--- Скачивание для: '{keyword}' ---")
        
        # Создаем папку для ключевого слова
        keyword_dir = output_path / keyword.replace(' ', '_')
        keyword_dir.mkdir(exist_ok=True)
        
        try:
            # Используем GoogleImageCrawler
            crawler = GoogleImageCrawler(
                storage={'root_dir': str(keyword_dir)},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=2,
            )
            
            crawler.crawl(
                keyword=keyword,
                max_num=num_images_per_keyword
            )
            
            # Ждем завершения
            time.sleep(10)
            
            # Проверяем скачанные файлы
            downloaded_files: List[Path] = []
            for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                downloaded_files.extend(keyword_dir.glob(f'*{ext}'))
                downloaded_files.extend(keyword_dir.glob(f'*{ext.upper()}'))
            
            all_downloaded_files.extend(downloaded_files)
            
        except Exception as e:
            print(f" Ошибка при скачивании '{keyword}': {e}")
            continue
    
    return all_downloaded_files