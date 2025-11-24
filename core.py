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
    """Фильтрует изображения по разрешению."""
    
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

    for name, crawler_cls in sources:
        now = count_images()
        if now >= target_count:
            break

        need = target_count - now
        batch = min(need * 3, 900)

        crawler = crawler_cls(
            storage={"root_dir": save_dir},
            downloader_threads=2,
            feeder_threads=1,
            parser_threads=1
        )

        before = count_images()
        try:
            crawler.crawl(keyword=keyword, max_num=batch)
        except Exception:
            pass
        time.sleep(1)
        after = count_images()

    remaining = filter_by_resolution(save_dir, min_res, max_res)

    while remaining < target_count:
        need = target_count - remaining

        for _, crawler_cls in sources:
            if count_images() >= target_count:
                break

            crawler = crawler_cls(storage={"root_dir": save_dir})
            try:
                crawler.crawl(keyword=keyword, max_num=need * 2)
            except Exception:
                pass

            time.sleep(1)
            remaining = filter_by_resolution(save_dir, min_res, max_res)


def create_annotation_csv(img_folder: str, output_csv: str) -> int:
    """Создает CSV файл с аннотациями изображений."""
    allowed = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    root = Path(img_folder).resolve()
    rows: List[Dict[str, Any]] = []

    for f in sorted(os.listdir(img_folder)):
        if Path(f).suffix.lower() in allowed:
            abs_p = str(root / f)
            rel_p = os.path.relpath(abs_p, start=os.getcwd())
            rows.append({
                "filename": f,
                "absolute_path": abs_p,
                "relative_path": rel_p
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "absolute_path", "relative_path"])
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)