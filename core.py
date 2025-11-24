import csv
import os
import time
from pathlib import Path
from typing import Tuple, List, Dict, Any

from PIL import Image
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler


def filter_by_resolution(folder: str,
                         min_res: Tuple[int, int],
                         max_res: Tuple[int, int]) -> int:
    """
    Фильтрует изображения по разрешению.
    Возвращает количество оставшихся изображений.
    """

    allowed_ext = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    time.sleep(0.8) 

    files = [
        f for f in os.listdir(folder)
        if Path(f).suffix.lower() in allowed_ext
    ]

    kept, removed = 0, 0
    for name in files:
        path = os.path.join(folder, name)

        try:
            with Image.open(path) as img:
                w, h = img.size

            if not (min_res[0] <= w <= max_res[0] and min_res[1] <= h <= max_res[1]):
                os.remove(path)
                removed += 1
            else:
                kept += 1

        except Exception:
            try:
                os.remove(path)
                removed += 1
            except Exception:
                pass

    return kept


def download_images(keyword: str,
                    target_count: int,
                    min_res: Tuple[int, int],
                    max_res: Tuple[int, int],
                    save_dir: str) -> None:
    """Загрузка изображений из нескольких источников с повторными попытками."""

    save_dir = "try_image"
    os.makedirs(save_dir, exist_ok=True)

    valid_ext = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

    def count_images() -> int:
        return len([f for f in os.listdir(save_dir)
                    if Path(f).suffix.lower() in valid_ext])

    sources = [
        ("Google", GoogleImageCrawler),
        ("Bing", BingImageCrawler),
        ("Baidu", BaiduImageCrawler)
    ]

    print("=== Начальная загрузка изображений ===")
    
    for name, crawler_cls in sources:
        now = count_images()
        if now >= target_count:
            print(f"Достигнуто целевое количество. Текущее: {now}, целевое: {target_count}")
            break

        need = target_count - now
        batch = min(need * 3, 900)

        print(f"Загрузка из {name}, нужно: {need} изображений, батч: {batch}")
        crawler = crawler_cls(
            storage={"root_dir": save_dir},
            downloader_threads=2,
            feeder_threads=1,
            parser_threads=1
        )

        before = count_images()
        
        try:
            crawler.crawl(keyword=keyword, max_num=batch)
        except Exception as e:
            print(f"Ошибка при загрузке из {name}: {e}")
        
        time.sleep(1)
        
        after = count_images()
        downloaded = after - before
        print(f"Загружено из {name}: {downloaded} изображений")

    remaining = filter_by_resolution(save_dir, min_res, max_res)
    print(f"После первоначальной фильтрации: {remaining} изображений")
    print("\n=== Проверка необходимости дополнительной загрузки ===")
    
    remaining = filter_by_resolution(save_dir, min_res, max_res)
    attempt = 1
    
    while remaining < target_count:
        need = target_count - remaining
        print(f"Попытка {attempt}: нужно дополнительно {need} изображений")
        
        for source_name, crawler_cls in sources:
            current_count = count_images()
            if current_count >= target_count:
                print(f"Достигнуто целевое количество: {current_count}")
                break
                
            print(f"Дополнительная загрузка из {source_name}")
        
            crawler = crawler_cls(storage={"root_dir": save_dir})
            
            try:
                crawler.crawl(keyword=keyword, max_num=need * 2)
            except Exception as e:
                print(f"Ошибка при дополнительной загрузке из {source_name}: {e}")
            
            time.sleep(1)
            
            remaining = filter_by_resolution(save_dir, min_res, max_res)
            
            if remaining >= target_count:
                print(f"Достигнуто целевое количество после дополнительной загрузки: {remaining}")
                break
        
        attempt += 1
        
        if attempt > 5:
            print(f"Достигнут лимит попыток. Текущее количество: {remaining}, целевое: {target_count}")
            break
            
        time.sleep(2)

    final_count = count_images()
    print(f"\n=== Итоговый результат ===")
    print(f"Целевое количество: {target_count}")
    print(f"Фактическое количество: {final_count}")
    
    if final_count >= target_count:
        print(" Загрузка завершена успешно!")
    else:
        print(f"  Загружено только {final_count} из {target_count} изображений")