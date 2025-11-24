"""Модуль для получения данных о звуках людей с веб-страниц."""
from bs4 import BeautifulSoup
import requests
import time
from typing import List, Dict, Optional
from settings import REQUEST_HEADERS


def get_web_content(url: str, timeout: int = 10) -> Optional[str]:
    """
    Получает HTML контент по указанному URL.

    Args:
        url: URL для запроса
        timeout: Таймаут запроса в секундах

    Returns:
        HTML контент или None в случае ошибки
    """
    try:
        response = requests.get(
            url, headers=REQUEST_HEADERS, timeout=timeout
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None


def parse_human_sounds(html_content: str) -> List[Dict[str, str]]:
    """
    Извлекает информацию о звуках людей из HTML.

    Args:
        html_content: HTML контент страницы

    Returns:
        Список словарей с информацией о звуках
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        human_sounds = []

        for element in soup.find_all(
            attrs={"data-audio-player-preview-url-value": True}
        ):
            audio_url = element.get("data-audio-player-preview-url-value")
            name = element.get("title", "Human Sound")

            if audio_url and audio_url.startswith("http"):
                human_sounds.append({
                    "name": name,
                    "audio_url": audio_url,
                })

        return human_sounds
    except Exception as e:
        print(f"Ошибка при парсинге HTML: {e}")
        return []


def collect_human_sounds(url: str) -> List[Dict[str, str]]:
    """
    Собирает звуки людей с нескольких страниц.

    Args:
        url: Базовый URL для сбора звуков

    Returns:
        Список словарей с информацией о звуках
    """
    try:
        sounds = []
        page_count = 5

        for page_num in range(1, page_count + 1):
            if page_num == 1:
                current_url = url
            else:
                current_url = f"{url}page/{page_num}/"

            html_content = get_web_content(current_url)
            if not html_content:
                continue

            page_sounds = parse_human_sounds(html_content)
            sounds.extend(page_sounds)

            time.sleep(1)

        return sounds
    except Exception as e:
        print(f"Ошибка при сборе звуков: {e}")
        return []