import os
import random
from pathlib import Path
from typing import List, Tuple
from icrawler.builtin import BingImageCrawler


class BearImageDownloader:
    """Класс для скачивания изображений медведей"""

    def __init__(self) -> None:
        # Специфичные ключевые слова для медведей-животных
        self.bear_keywords = [
            "brown bear animal",
            "grizzly bear wildlife",
            "ursus arctos",
            "bear mammal nature",
            "wild bear forest",
            "european brown bear",
            "bear species animal",
            "bear wildlife photography",
            "bear in natural habitat",
            "bear cubs playing"
        ]

    def download_images(
            self,
            date_ranges: List[Tuple[str, str]],
            images_per_range: List[int],
            output_dir: str
    ) -> List[str]:
        """Скачивает изображения медведей"""
        os.makedirs(output_dir, exist_ok=True)

        all_images = []
        total_target = sum(images_per_range)

        print(f"Цель: {total_target} изображений медведей")

        # Скачиваем для каждого диапазона
        for i, (start_date, end_date) in enumerate(date_ranges):
            target = images_per_range[i]
            downloaded = self._download_range(start_date, end_date, target, output_dir, i)
            all_images.extend(downloaded)
            print(f"Диапазон {i + 1}: {len(downloaded)}/{target} изображений")

        final_count = len(all_images)
        print(f"Итог: {final_count} изображений медведей")

        if final_count >= 50:
            print("✓ Достигнут минимум 50 изображений!")
        else:
            print(f"✗ Скачано только {final_count} изображений")

        return all_images

    def _download_range(
            self,
            start_date: str,
            end_date: str,
            target: int,
            output_dir: str,
            range_idx: int
    ) -> List[str]:
        """Скачивает для одного диапазона"""
        range_dir = os.path.join(output_dir, f"range_{range_idx + 1}")
        os.makedirs(range_dir, exist_ok=True)

        # Очищаем папку
        self._clean_folder(range_dir)

        try:
            # Используем специфичные ключевые слова для животных
            keyword = random.choice(self.bear_keywords)

            # Добавляем фильтр по датам
            search_query = f"{keyword} after:{start_date} before:{end_date}"

            print(f"  Поиск: '{search_query}'")

            crawler = BingImageCrawler(storage={'root_dir': range_dir})
            crawler.crawl(keyword=search_query, max_num=target + 5)

        except Exception as e:
            print(f"  Ошибка: {e}")

        return self._get_images(range_dir)[:target]

    def _clean_folder(self, directory: str):
        """Очищает папку"""
        if os.path.exists(directory):
            for file in Path(directory).glob('*'):
                try:
                    file.unlink()
                except:
                    pass

    def _get_images(self, directory: str) -> List[str]:
        """Получает список изображений"""
        images = []
        for file in Path(directory).glob('*'):
            if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                images.append(str(file.resolve()))
        return images