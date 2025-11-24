

from duckduckgo_search import DDGS
import requests
import os
import time
import random
from typing import List

def create_download_directory(directory: str = "downloaded_images") -> str:
    """
    Создает директорию для скачанных изображений, если она не существует.

    Args:
        directory (str): Имя директории для сохранения изображений.

    Returns:
        str: Путь к созданной директории.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✅ Создана директория: {directory}")
    else:
        print(f"📁 Директория уже существует: {directory}")
    return directory


def get_image_urls_duckduckgo(
    keyword: str,
    max_results: int = 200
) -> List[str]:
    """
    Получает URL-ы изображений через DuckDuckGo Images.

    Args:
        keyword (str): Поисковый запрос (например, 'monkey animal wildlife').
        max_results (int): Максимальное количество URL-ов для получения.

    Returns:
        List[str]: Список уникальных URL-ов изображений.
    """
    print(f"🔍 Поиск в DuckDuckGo по запросу: '{keyword}' (до {max_results} результатов)")

    try:
       
        ddgs = DDGS()

        
        results = ddgs.images(
            keywords=keyword,
            region="wt-wt",     
            safesearch="off",    
            max_results=max_results
        )

        urls = []
        for item in results:
            if isinstance(item, dict) and 'image' in item:
                url = item['image']
                if url.startswith('http'):
                    urls.append(url)

        unique_urls = list(dict.fromkeys(urls))  
        print(f"✅ Получено {len(unique_urls)} уникальных URL-ов.")
        return unique_urls

    except Exception as e:
        print(f"⚠️ Ошибка при поиске через DuckDuckGo: {e}")
        return []


def download_images(
    urls: List[str],
    save_dir: str,
    min_num: int = 50,
    timeout: int = 10
) -> int:
    """
    Скачивает изображения по списку URL-ов.

    Args:
        urls (List[str]): Список URL-ов.
        save_dir (str): Путь к папке для сохранения.
        min_num (int): Минимальное количество изображений для скачивания.
        timeout (int): Таймаут запроса в секундах.

    Returns:
        int: Количество успешно скачанных изображений.
    """
    downloaded = 0
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    for i, url in enumerate(urls, 1):
        if downloaded >= min_num:
            break

        
        ext = '.jpg'
        if url.lower().endswith(('.png', '.jpeg', '.gif', '.bmp', '.webp')):
            ext = url[url.rfind('.'):].lower()

        filename = f"image_{downloaded + 1:04d}{ext}"
        filepath = os.path.join(save_dir, filename)

        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()

          
            content_type = resp.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                print(f"⚠️ Пропускаем (не изображение): {url[:50]}...")
                continue

            with open(filepath, 'wb') as f:
                f.write(resp.content)

            downloaded += 1
            print(f"✅ {downloaded}/{min_num} — {filename}")

        except Exception as e:
            print(f"❌ Не удалось скачать {url[:50]}...: {type(e).__name__}")
            continue

        
        time.sleep(random.uniform(0.2, 0.8))

    return downloaded


def download_monkey_images(
    keyword: str = "monkey",
    max_num: int = 100,
    min_num: int = 50,
    year: int = 2025
) -> str:
    """
    Скачивает изображения по ключевому слову с фильтрацией по году.
    Гарантирует минимум min_num изображений.
        Args:
        keyword (str): Базовое ключевое слово.
        max_num (int): Максимальное количество (влияет на лимит поиска).
        min_num (int): Минимальное количество (≥50).
        year (int): Год для фильтрации (добавляется в запрос).

    Returns:
        str: Путь к директории с изображениями.

    Raises:
        ValueError: При неверных параметрах.
        RuntimeError: Если не удалось достичь min_num.
    """
    
    if not (50 <= min_num <= 1000):
        raise ValueError("min_num должен быть в диапазоне [50, 1000]")
    if not (50 <= max_num <= 1000):
        raise ValueError("max_num должен быть в диапазоне [50, 1000]")
    if min_num > max_num:
        raise ValueError("min_num не может быть больше max_num")

    try:
        download_dir = create_download_directory()

        
        search_query = f"{keyword} animal wildlife {year}"
        print(f"🎯 Уточнённый поисковый запрос: '{search_query}'")

        
        urls = get_image_urls_duckduckgo(search_query, max_results=max_num * 2)

        if len(urls) < min_num:
            
            fallback_query = f"{keyword} animal wildlife"
            print(f"🔁 Попытка без года: '{fallback_query}'")
            urls += get_image_urls_duckduckgo(fallback_query, max_results=max_num)

        urls = list(dict.fromkeys(urls))  

        if len(urls) < min_num:
            raise RuntimeError(
                f"❌ Найдено только {len(urls)} URL-ов, требуется ≥ {min_num}."
            )

       
        count = download_images(urls, download_dir, min_num=min_num)

        if count < min_num:
            raise RuntimeError(f"❌ Скачано только {count} изображений, требуется ≥ {min_num}.")

        print(f"🎉 Успешно скачано {count} изображений.")
        return download_dir

    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        raise