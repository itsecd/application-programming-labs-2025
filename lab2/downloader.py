import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List
from annotation import create_annotation

class MusicDownloader:
    """
    Класс для парсинга и скачивания аудиофайлов с mixkit.co по длительности.
    """

    BASE_URL = "https://mixkit.co/free-stock-music/"

    def __init__(self, download_dir: str):
        """
        Инициализация загрузчика, подготовка директории и HTTP-сессии.
        :param download_dir: путь к директории для сохранения аудиофайлов
        """
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })

    def parse_duration(self, duration_str: str) -> int:
        """
        Преобразует строку 'm:ss' в секунды.
        :param duration_str: строка длительности
        :return: длительность в секундах, либо 0 при ошибке"""
        try:
            minutes, seconds = map(int, duration_str.strip().split(":"))
            return minutes * 60 + seconds
        except Exception:
            return 0

    def get_tracks_from_page(self, min_sec: int, max_sec: int) -> List[dict]:
        """
        Парсит страницу mixkit и возвращает список треков с прямыми ссылками и длительностью.
        :param min_sec: минимальная длительность трека в секундах
        :param max_sec: максимальная длительность трека в секундах
        :return: список треков в виде словарей (title, duration, url)
        """
        url = self.BASE_URL
        response = self.session.get(url)
        if not response.ok:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.item-grid__item")
        tracks = []

        for item in items:
            title_el = item.select_one("h2.item-grid-card__title")
            duration_el = item.select_one('div[data-test-id="duration"]')
            player_el = item.select_one('div[data-test-id="audio-player"]')

            if not all([title_el, duration_el, player_el]):
                continue

            title = title_el.get_text(strip=True)
            duration = self.parse_duration(duration_el.get_text(strip=True))
            mp3_url = player_el.get("data-audio-player-preview-url-value")

            if not mp3_url or not mp3_url.startswith("http"):
                mp3_url = f"https://mixkit.co{mp3_url}"

            if min_sec <= duration <= max_sec:
                tracks.append({
                    "title": title,
                    "duration": duration,
                    "url": mp3_url
                })

        return tracks
    
    def download_file(self, url: str, save_path: str) -> bool:
        """
        Скачивает файл по ссылке и сохраняет на диск.
        :param url: прямая ссылка на MP3-файл
        :param save_path: путь сохранения файла
        :return: True если успешно, иначе False
        """
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            return True
        except Exception:
            if os.path.exists(save_path):
                os.remove(save_path)
            return False

    def download_music(self, count: int, min_sec: int, max_sec: int, csv_path: str) -> None:
        """
        Ищет треки по длительности, скачивает нужное количество и создаёт аннотацию.
        :param count: количество треков для скачивания
        :param min_sec: минимальная длительность трека в секундах
        :param max_sec: максимальная длительность трека в секундах
        :param csv_path: путь сохранения CSV-аннотации
        :return: None
        """
        print(f"🔍 Поиск треков длительностью от {min_sec} до {max_sec} секунд...")

        found_tracks = self.get_tracks_from_page(min_sec, max_sec)
        
        found_tracks = found_tracks[:count]

        if not found_tracks:
            print("⚠️ Не найдено треков подходящей длительности.")
            create_annotation([], csv_path)
            return

        print(f"🎧 Найдено {len(found_tracks)} треков. Начинаем загрузку...")

        downloaded_paths = []
        for i, track in enumerate(found_tracks, 1):
            safe_title = re.sub(r"[^\w\s-]", "", track["title"]).replace(" ", "_")[:80]
            save_path = os.path.join(self.download_dir, f"{i:03d}_{safe_title}.mp3")
            if self.download_file(track["url"], save_path):
                print(f"  ✅ [{i}] {track['title']} ({track['duration']} сек)")
                downloaded_paths.append(save_path)
            else:
                print(f"  ❌ Ошибка скачивания: {track['title']}")

        create_annotation(downloaded_paths, csv_path)
        print(f"🧾 Аннотация создана: {csv_path}")