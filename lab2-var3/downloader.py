from __future__ import annotations
import os
import random
import time
from pathlib import Path
from typing import List, Tuple, Set
from icrawler.builtin import BingImageCrawler

from utils import cleanup_directory, image_matches_size


def download_images(
    output_dir: str,
    size_ranges: List[Tuple[int, int]],
    counts: List[int]
) -> List[Tuple[str, str]]:
    """
    Скачивает изображения согласно диапазонам размеров и количеству.
    Возвращает список пар (absolute_path, relative_path).
    """

    os.makedirs(output_dir, exist_ok=True)

    all_files: List[Tuple[str, str]] = []
    all_abs: Set[str] = set()

    keywords = [
        'fish', 'fishes', 'aquarium fish',
        'colorful fish', 'tropical fish', 'marine fish'
    ]

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}

    for i, ((min_size, max_size), need_count) in enumerate(zip(size_ranges, counts)):
        range_dir = os.path.join(output_dir, f"range_{i+1}")
        os.makedirs(range_dir, exist_ok=True)

        cleanup_directory(range_dir)

        downloaded_count = 0
        attempts = 0

        while downloaded_count < need_count and attempts < 6:
            attempts += 1
            keyword = random.choice(keywords)
            request_num = max(1, (need_count - downloaded_count) * (2 if attempts == 1 else 1))

            try:
                crawler = BingImageCrawler(
                    storage={'root_dir': range_dir},
                    feeder_threads=3,
                    parser_threads=3,
                    downloader_threads=6
                )
                crawler.crawl(keyword=keyword, max_num=request_num, file_idx_offset='auto')

            except Exception:
                continue

            cleanup_directory(range_dir)

            new_files = []
            for file_path in Path(range_dir).rglob("*.*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in image_exts:
                    continue
                if file_path.stat().st_size <= 10240:
                    continue
                if not image_matches_size(str(file_path), min_size, max_size):
                    continue

                abs_p = str(file_path.absolute())
                if abs_p not in all_abs:
                    rel_p = str(file_path.relative_to(output_dir))
                    new_files.append((abs_p, rel_p))
                    all_abs.add(abs_p)

            added = min(len(new_files), need_count - downloaded_count)
            all_files.extend(new_files[:added])
            downloaded_count += added

            if downloaded_count < need_count:
                time.sleep(1)

    return all_files