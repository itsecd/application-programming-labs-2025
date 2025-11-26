from icrawler.builtin import BingImageCrawler
from typing import List
from pathlib import Path
import os
import time

def download_images_by_keywords(
    keywords: List[str],
    output_dir: str,
    per_keyword_count: int
) -> None:
    """
    Скачивает ровно per_keyword_count изображений по каждому ключевому слову через Bing.

    Args:
        keywords (List[str]): Список ключевых слов
        output_dir (str): Путь к директории для сохранения
        per_keyword_count (int): Точное количество изображений на ключевое слово
    """
    output_path = Path(output_dir).resolve()

    for keyword in keywords:
        print(f"\n Цель: скачать ровно {per_keyword_count} изображений для '{keyword}'")
        keyword_dir = output_path / keyword
        keyword_dir.mkdir(parents=True, exist_ok=True)

        attempt = 0
        max_attempts = 5
        downloaded_count = 0

        while downloaded_count < per_keyword_count and attempt < max_attempts:
            current_files = list(keyword_dir.glob("*"))
            downloaded_count = len(current_files)
            needed = per_keyword_count - downloaded_count

            if needed <= 0:
                break

            attempt += 1
            print(f"  Попытка {attempt}: нужно ещё {needed} изображений...")

            try:
                request_count = max(needed, 10)

                crawler = BingImageCrawler(
                    storage={'root_dir': str(keyword_dir)},
                    parser_threads=2,
                    downloader_threads=4,
                    log_level='WARNING'
                )

                crawler.crawl(
                    keyword=keyword,
                    max_num=request_count,
                    filters={
                        'size': 'medium',
                        'type': 'photo'
                    }
                )

                time.sleep(1)

                new_files = list(keyword_dir.glob("*"))
                downloaded_count = len(new_files)
                print(f"    Теперь в папке: {downloaded_count} файлов")

            except Exception as e:
                print(f"    ⚠️ Ошибка на попытке {attempt}: {e}")

        final_count = len(list(keyword_dir.glob("*")))
        if final_count == per_keyword_count:
            print(f"✅ '{keyword}': ровно {final_count} изображений.")
        elif final_count > per_keyword_count:
            files = sorted(keyword_dir.glob("*"), key=lambda x: x.stat().st_ctime)
            for extra_file in files[per_keyword_count:]:
                extra_file.unlink()
                print(f"    Удалён лишний файл: {extra_file.name}")
            print(f"✅ '{keyword}': оставлено ровно {per_keyword_count} изображений.")
        else:
            print(f"⚠️ '{keyword}': удалось скачать только {final_count} из {per_keyword_count}.")