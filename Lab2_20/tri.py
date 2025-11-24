"""
Модуль для парсинга и скачивания звуков транспорта с сайта mixkit.co.
"""

import os
import re
import requests
import time
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class AudioDownloader:
    """Класс для парсинга и скачивания звуков транспорта с mixkit.co."""

    def __init__(self, download_dir: str):
        """Инициализация загрузчика с указанием директории для сохранения."""
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        os.makedirs(download_dir, exist_ok=True)

    def download_transport_audio(self, count: int) -> int:
        """Скачиваем указанное количество звуков транспорта."""
        print(f"Поиск звуков транспорта...")

        # Основные категории транспорта на Mixkit
        transport_categories = [
            "car", "vehicle", "transport", "traffic", "motor",
            "engine", "horn", "siren", "ambulance", "fire-truck",
            "police", "bus", "truck", "motorcycle", "bicycle",
            "train", "metro", "airplane", "airport", "helicopter",
            "boat", "ship", "subway", "taxi"
        ]

        total_downloaded = 0
        
        for category in transport_categories:
            if total_downloaded >= count:
                break
                
            remaining = count - total_downloaded
            url = f"https://mixkit.co/free-sound-effects/{category}/"
            
            print(f"Поиск в категории: {category}")

            try:
                tracks = self._parse_tracks_from_url(url, remaining)

                if not tracks:
                    continue

                print(f"Найдено {len(tracks)} треков в категории '{category}'")

                for i, track in enumerate(tracks, 1):
                    if total_downloaded >= count:
                        break

                    if self._download_single_track(track, category, total_downloaded + 1):
                        total_downloaded += 1
                        print(f"Скачано: {total_downloaded}/{count}")

                    # Пауза между скачиваниями
                    time.sleep(random.uniform(0.5, 1.5))

            except Exception as e:
                print(f"Ошибка обработки категории {category}: {e}")
                continue

        return total_downloaded

    def _parse_tracks_from_url(self, url: str, max_tracks: int) -> List[Dict[str, str]]:
        """Парсим звуки со страницы категории транспорта."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            tracks = self._extract_tracks_from_html(soup)

            return tracks[:max_tracks]

        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            return []
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            return []

    def _extract_tracks_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлекаем информацию о звуках из HTML."""
        tracks = []
        
        
        audio_elements = soup.find_all('audio')
        
        for audio in audio_elements:
            track = self._extract_track_from_audio(audio)
            if track:
                tracks.append(track)

        # Также ищем аудиоэлементы в data-атрибутах
        player_elements = soup.find_all('div', {'data-audio-player-preview-url-value': True})
        for player in player_elements:
            track = self._extract_track_from_player(player)
            if track:
                tracks.append(track)

        return tracks

    def _extract_track_from_audio(self, audio_element) -> Optional[Dict[str, str]]:
        """Извлекаем информацию о звуке из audio элемента."""
        try:
            source = audio_element.find('source')
            if not source or not source.get('src'):
                return None

            mp3_url = source['src']
            if not mp3_url.startswith('http'):
                mp3_url = urljoin('https://mixkit.co', mp3_url)

            # Получаем название из родительских элементов
            title_element = audio_element.find_previous(['h3', 'h4', 'div'], class_=re.compile(r'title|name', re.I))
            title = title_element.get_text(strip=True) if title_element else "transport_sound"

            return {"title": title, "url": mp3_url}

        except Exception:
            return None

    def _extract_track_from_player(self, player_element) -> Optional[Dict[str, str]]:
        """Извлекаем информацию о звуке из player элемента."""
        try:
            mp3_url = player_element.get('data-audio-player-preview-url-value')
            if not mp3_url:
                return None

            if not mp3_url.startswith('http'):
                mp3_url = urljoin('https://mixkit.co', mp3_url)

            title_element = player_element.find_previous(['h3', 'h4'], class_=re.compile(r'title', re.I))
            title = title_element.get_text(strip=True) if title_element else "transport_sound"

            return {"title": title, "url": mp3_url}

        except Exception:
            return None

    def _download_single_track(self, track: Dict[str, str], category: str, index: int) -> bool:
        """Скачиваем один звуковой файл."""
        safe_title = self._create_safe_filename(track["title"])
        filename = f"transport_{index:03d}_{safe_title}.mp3"
        filepath = os.path.join(self.download_dir, filename)

        if os.path.exists(filepath):
            print(f"Файл уже существует: {filename}")
            return True

        try:
            response = self.session.get(track["url"], timeout=30, stream=True)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            file_size = os.path.getsize(filepath)
            if file_size > 1024:  # Минимум 1KB
                print(f"Скачан: {filename} ({file_size} байт)")
                return True
            else:
                os.remove(filepath)
                print(f"Файл слишком маленький: {filename}")
                return False

        except Exception as e:
            print(f"Ошибка при скачивании {filename}: {e}")
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
            return False

    def _create_safe_filename(self, name: str) -> str:
        """Создаем безопасное имя файла."""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '_', name)
        name = name.strip('_.')
        return name[:50] if name else "sound"

    def get_downloaded_files_info(self) -> List[Dict[str, str]]:
        """Возвращаем информацию о всех скачанных файлах."""
        files_info = []

        try:
            for filename in os.listdir(self.download_dir):
                if filename.endswith('.mp3'):
                    abs_path = os.path.abspath(os.path.join(self.download_dir, filename))
                    rel_path = os.path.relpath(abs_path)

                    files_info.append({
                        'filename': filename,
                        'absolute_path': abs_path,
                        'relative_path': rel_path
                    })

        except Exception as e:
            print(f"Ошибка чтения директории: {e}")

        return files_info