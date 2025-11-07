import csv
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image
from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler


def filter_images_by_size(image_dir: str, min_size: Tuple[int, int], max_size: Tuple[int, int]) -> int:
    """Удаляет изображения, не соответствующие диапазону размеров"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    removed_count: int = 0
    kept_count: int = 0

    time.sleep(1)
    files_to_process: List[str] = [
        f for f in os.listdir(image_dir)
        if Path(f).suffix.lower() in image_extensions
    ]

    print(f"\nПроверка {len(files_to_process)} изображений...")

    for filename in files_to_process:
        filepath = os.path.join(image_dir, filename)
        try:
            with Image.open(filepath) as img:
                width, height = img.size
            if (width < min_size[0] or height < min_size[1] or
                    width > max_size[0] or height > max_size[1]):
                os.remove(filepath)
                removed_count += 1
            else:
                kept_count += 1
        except Exception:
            try:
                os.remove(filepath)
                removed_count += 1
            except Exception:
                pass

    print(f"Фильтрация завершена: оставлено {kept_count}, удалено {removed_count}")
    return kept_count


def download_images(keyword: str, num_images: int, min_size: Tuple[int, int],
                   max_size: Tuple[int, int], save_dir: str) -> None:
    """Загружает изображения с Baidu, Bing, Google."""
    os.makedirs(save_dir, exist_ok=True)
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    def get_current_count() -> int:
        return len([
            f for f in os.listdir(save_dir)
            if Path(f).suffix.lower() in image_extensions
        ])

    need_count: int = num_images
    sources: List[Tuple[str, Any]] = [
        ("Baidu", BaiduImageCrawler),
        ("Bing", BingImageCrawler),
        ("Google", GoogleImageCrawler)
    ]

    for source_name, crawler_class in sources:
        current_count: int = get_current_count()
        if current_count >= need_count:
            print(f"\nДостигнуто {current_count} изображений, загрузка завершена")
            break

        remaining: int = need_count - current_count
        download_count: int = min(remaining * 3, 1000)
        print(f"\nИсточник: {source_name}, необходимо ещё {remaining} изображений")

        crawler = crawler_class(
            storage={'root_dir': save_dir},
            downloader_threads=2,
            parser_threads=1,
            feeder_threads=1
        )

        before: int = get_current_count()
        try:
            crawler.crawl(keyword=keyword, max_num=download_count)
        except Exception as e:
            print(f"Ошибка при работе с {source_name}: {e}")

        time.sleep(2)
        after: int = get_current_count()
        print(f"Загружено с {source_name}: {after - before}, всего: {after}")

        if after >= need_count:
            break

    total_downloaded: int = get_current_count()
    print(f"\nФильтрация по размеру: от {min_size} до {max_size}")
    remaining: int = filter_images_by_size(save_dir, min_size, max_size)
    print(f"Осталось изображений после фильтрации: {remaining}")

    while remaining < need_count:
        shortage: int = need_count - remaining
        print(f"\nНедостача после фильтрации: {shortage} изображений")
        for source_name, crawler_class in sources:
            if get_current_count() >= need_count:
                break
            print(f"\nДокачка через {source_name}")
            crawler = crawler_class(storage={'root_dir': save_dir})
            try:
                crawler.crawl(keyword=keyword, max_num=shortage * 2)
            except Exception as e:
                print(f"Ошибка: {e}")
            time.sleep(2)
            remaining = filter_images_by_size(save_dir, min_size, max_size)
            print(f"Теперь доступно: {remaining}")

    print(f"\nИтого: {get_current_count()} файлов сохранено в {save_dir}")


def create_annotation_csv(image_dir: str, csv_path: str) -> int:
    """Создаёт CSV с метаданными изображений"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_dir_path: Path = Path(image_dir).resolve()
    files_info: List[Dict[str, Any]] = []

    for filename in sorted(os.listdir(image_dir)):
        if Path(filename).suffix.lower() in image_extensions:
            abs_path = str(image_dir_path / filename)
            rel_path = os.path.relpath(abs_path, start=os.getcwd())
            files_info.append({
                'filename': filename,
                'absolute_path': abs_path,
                'relative_path': rel_path
            })

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'absolute_path', 'relative_path'])
        writer.writeheader()
        writer.writerows(files_info)

    print(f"Создан CSV с {len(files_info)} записями: {csv_path}")
    return len(files_info)
