import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
from config import HEADERS


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

    container = soup.select_one("div.item-grid__items")
    if not container:
        container = soup.select_one("div.grid-cards")
    if not container:
        container = soup.select_one("div.sounds-grid")

    if container:
        for item in container.select("div.item-grid__item,"
                                     " div.grid-card, div.sound-card"):
            title_tag = item.select_one(
                "h2.item-grid-card__title, h3.card-title, h4.sound-title")
            if not title_tag:
                continue

            mp3_link = None

            player_tag = item.select_one(
                'div[data-audio-player-preview-url-value]')
            if player_tag:
                mp3_link = player_tag.get(
                    "data-audio-player-preview-url-value")

            if not mp3_link:
                mp3_element = item.select_one('[data-mp3]')
                if mp3_element:
                    mp3_link = mp3_element.get("data-mp3")

            if not mp3_link:
                audio_tag = item.select_one("audio source[src$='.mp3']")
                if audio_tag:
                    mp3_link = audio_tag.get("src")

            if mp3_link and mp3_link.startswith("http"):
                sounds.append({
                    "title": title_tag.get_text(strip=True),
                    "mp3_link": mp3_link,
                })

    if not sounds:
        players = soup.find_all(
            attrs={"data-audio-player-preview-url-value": True})
        for player in players:
            title = player.get("title") or "Animal Sound"
            mp3_link = player.get("data-audio-player-preview-url-value")
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
