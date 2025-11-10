from bs4 import BeautifulSoup
from config import HEADERS
import requests
import time
from typing import List, Dict


def fetch_page(url: str, timeout: int = 10) -> str | None:
    """
    Загружает HTML страницу по указанному URL.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def extract_animal_sounds_from_html(html: str) -> List[Dict[str, str]]:
    """
    Извлекает информацию о звуках животных из HTML страницы.
    """
    soup = BeautifulSoup(html, "html.parser")
    sounds = []

    for element in soup.find_all(
            attrs={"data-audio-player-preview-url-value": True}):
        mp3_link = element.get("data-audio-player-preview-url-value")
        title = element.get("title", "Animal Sound")

        if mp3_link and mp3_link.startswith("http"):
            sounds.append({
                "title": title,
                "mp3_link": mp3_link,
            })

    return sounds


def fetch_animal_sounds(url: str, num_sounds: int) -> List[Dict[str, str]]:
    """
    Собирает звуки животных со всех доступных страниц.
    """
    sounds = []
    total_pages = 1

    for page in range(1, total_pages + 1):
        if page == 1:
            page_url = url
        else:
            page_url = f"{url}page/{page}/"

        html = fetch_page(page_url)
        if not html:
            continue

        page_sounds = extract_animal_sounds_from_html(html)
        sounds.extend(page_sounds)

        if len(sounds) >= num_sounds:
            return sounds[:num_sounds]

        time.sleep(1)

    return sounds
