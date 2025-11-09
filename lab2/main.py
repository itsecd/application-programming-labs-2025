"""
Лабораторная работа №2: Загрузка изображений по ключевому слову с фильтрацией по датам.
"""

from pathlib import Path
from typing import List, Tuple

from icrawler.builtin import GoogleImageCrawler


class ImageDownloadManager:
    """Управляет загрузкой изображений."""
    
    IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
    
    def download_images(self, keyword: str, output_dir: Path, 
                       date_range: Tuple[Tuple[int, int, int], Tuple[int, int, int]], 
                       max_num: int) -> bool:
        """Загружает изображения для указанного диапазона дат."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            crawler = GoogleImageCrawler(storage={'root_dir': str(output_dir)})
            crawler.crawl(keyword=keyword, filters={'date': date_range}, max_num=max_num)
            return True
        except Exception:
            return False


class ImagePathIterator:
    """Итератор для перебора путей к изображениям."""
    
    def __init__(self, source: str, root_dir: str = None) -> None:
        self._items: List[List[str]] = []
        self._index: int = 0
    
    def __iter__(self) -> 'ImagePathIterator':
        self._index = 0
        return self
    
    def __next__(self) -> List[str]:
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item