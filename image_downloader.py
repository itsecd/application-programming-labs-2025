import os
import time
from pathlib import Path
from typing import List, Tuple
from icrawler.builtin import BingImageCrawler


class BearImageDownloader:
    """Класс для скачивания изображений медведей с гарантией минимума 50."""
    
    def __init__(self) -> None:
        self.bear_keywords = [
            "brown bear",
            "grizzly bear", 
            "ursus arctos",
            "bear animal",
            "wild bear",
            "bear wildlife",
            "bear forest",
            "bear mammal",
            "bear nature",
            "bear species"
        ]
    
    def download_images(
        self, 
        date_ranges: List[Tuple[str, str]], 
        images_per_range: List[int],
        output_dir: str
    ) -> List[str]:
        """Скачивает изображения медведей с гарантией минимума 50."""
        os.makedirs(output_dir, exist_ok=True)
        self._clean_directory(output_dir)
        
        total_target = sum(images_per_range)
        print(f"Целевое количество: {total_target} изображений медведей")
        
        all_images = []
        

        for range_idx, (start_date, end_date) in enumerate(date_ranges):
            target_count = images_per_range[range_idx]
            
            range_dir = os.path.join(output_dir, f"range_{range_idx + 1}")
            os.makedirs(range_dir, exist_ok=True)
            
            print(f"\nДиапазон {range_idx + 1}: {start_date} - {end_date}")
            print(f"Цель: {target_count} изображений")
            
            downloaded = self._download_for_range(
                start_date, end_date, target_count, range_dir
            )
            all_images.extend(downloaded)
            
            print(f"Скачано: {len(downloaded)}")
            print(f"Общий прогресс: {len(all_images)}/{total_target}")
        
        """ГАРАНТИЯ: если меньше 50, докачиваем до 50"""
        if len(all_images) < 50:
            print(f"\nВНИМАНИЕ: Скачано только {len(all_images)} изображений")
            print("Докачиваем до 50...")
            
            needed = 50 - len(all_images)
            additional = self._download_additional(needed, output_dir)
            all_images.extend(additional)
            
            print(f"Докачано: {len(additional)} изображений")
        
        
        result = all_images[:total_target]
        final_count = len(result)
        
        print(f"\nФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {final_count} изображений медведей")
        
        if final_count >= 50:
            print("УСПЕХ: Достигнут минимум 50 изображений!")
        else:
            print("Не удалось достичь 50 изображений")
        
        return result
    
    def _download_for_range(
        self, 
        start_date: str, 
        end_date: str, 
        target_count: int, 
        output_dir: str
    ) -> List[str]:
        """Скачивает изображения для одного диапазона"""
        downloaded_files = []
        existing_files = set(self._get_existing_images(output_dir))
        
        for keyword in self.bear_keywords:
            if len(downloaded_files) >= target_count:
                break
                
            needed = target_count - len(downloaded_files)
            print(f"Поиск: '{keyword}'")
            
            try:
                search_queries = [
                    f"{keyword} after:{start_date} before:{end_date}",
                    keyword  
                ]
                
                for query in search_queries:
                    if len(downloaded_files) >= target_count:
                        break
                    
                    crawler = BingImageCrawler(storage={'root_dir': output_dir})
                    crawler.crawl(keyword=query, max_num=needed + 10)
                    
                    time.sleep(1)
                    
                    
                    current_files = self._get_existing_images(output_dir)
                    new_files = [f for f in current_files if f not in existing_files]
                    
                    if new_files:
                        downloaded_files.extend(new_files)
                        existing_files.update(new_files)
                        print(f"Найдено: {len(new_files)}")
                        break  
                    
            except Exception as e:
                print(f"    Ошибка: {e}")
        
        return downloaded_files[:target_count]
    
    def _download_additional(self, needed: int, output_dir: str) -> List[str]:
        """Докачивает дополнительные изображения без ограничений по датам."""
        print(f"\nДополнительное скачивание: нужно {needed} изображений")
        
        additional_dir = os.path.join(output_dir, "additional")
        os.makedirs(additional_dir, exist_ok=True)
        
        downloaded_files = []
        existing_files = set()
        
        """Более общие запросы для докачивания"""
        general_keywords = [
            "bear",
            "brown bear", 
            "grizzly bear",
            "wildlife bear",
            "animal bear"
        ]
        
        for keyword in general_keywords:
            if len(downloaded_files) >= needed:
                break
                
            current_needed = needed - len(downloaded_files)
            print(f"  Доп. поиск: '{keyword}'")
            
            try:
                crawler = BingImageCrawler(storage={'root_dir': additional_dir})
                crawler.crawl(keyword=keyword, max_num=current_needed + 20)
                
                time.sleep(1)
                
                current_files = self._get_existing_images(additional_dir)
                new_files = [f for f in current_files if f not in existing_files]
                
                if new_files:
                    downloaded_files.extend(new_files)
                    existing_files.update(new_files)
                    print(f"Найдено: {len(new_files)}")
                    
            except Exception as e:
                print(f"Ошибка: {e}")
        
        return downloaded_files[:needed]
    
    def _clean_directory(self, directory: str) -> None:
        """Очищаю директорию"""
        if os.path.exists(directory):
            for file in Path(directory).rglob('*'):
                try:
                    file.unlink()
                except OSError:
                    pass
    
    def _get_existing_images(self, directory: str) -> List[str]:
        """Возвращаю список изображений в директории"""
        images = []
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                try:
                    
                    if os.path.getsize(file_path) > 5120:
                        images.append(str(file_path.resolve()))
                except OSError:
                    continue
        return images