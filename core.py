import os
import time
from pathlib import Path
from typing import Tuple

from PIL import Image
from icrawler.builtin import GoogleImageCrawler


def download_images_basic(keyword: str,
                         target_count: int,
                         min_res: Tuple[int, int],
                         max_res: Tuple[int, int],
                         save_dir: str) -> None:
    """Базовая загрузка изображений только из Google."""
    
    os.makedirs(save_dir, exist_ok=True)

    crawler = GoogleImageCrawler(
        storage={"root_dir": save_dir},
        downloader_threads=2
    )

    try:
        crawler.crawl(keyword=keyword, max_num=target_count * 2)
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")

    time.sleep(1)
    
    kept_count = filter_by_resolution(save_dir, min_res, max_res)
    print(f"Сохранилось изображений после фильтрации: {kept_count}")
    
    return kept_count