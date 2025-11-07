
"""
Модуль для парсинга и скачивания аудиофайлов с сайта mixkit.co.
"""

import os
import re
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class AudioDownloader:
    """Класс для парсинга и скачивания аудиофайлов с mixkit.co."""
    
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

    def download_instrument_audio(self, instrument: str, count: int) -> int:
        """Скачивает указанное количество аудиофайлов для инструмента."""
        print(f"Поиск аудио для {instrument}...")
        
        url = f"https://mixkit.co/free-stock-music/{instrument}/"
        
        try:
            tracks = self._parse_tracks_from_url(url, count)
            
            if not tracks:
                print(f"Не найдено треков для {instrument}")
                return 0
            
            print(f"Найдено {len(tracks)} треков для скачивания")
            downloaded_count = 0
            
            for i, track in enumerate(tracks, 1):
                if downloaded_count >= count:
                    break
                    
                if self._download_single_track(track, instrument, i):
                    downloaded_count += 1

            return downloaded_count
            
        except Exception as e:
            print(f"Ошибка обработки {instrument}: {e}")
            return 0

    def _parse_tracks_from_url(self, url: str, max_tracks: int) -> List[Dict[str, str]]:
        """Парсит треки со страницы инструмента."""
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
        """Извлекает информацию о треках из HTML."""
        tracks = []
        container = soup.select_one("div.item-grid__items")
        
        if not container:
            return tracks
        
        items = container.select("div.item-grid__item")
        
        for item in items:
            track = self._extract_track_from_item(item)
            if track:
                tracks.append(track)
        
        return tracks

    def _extract_track_from_item(self, item) -> Optional[Dict[str, str]]:
        """Извлекает информацию о треке из HTML элемента."""
        try:
            title_element = item.select_one("h2.item-grid-card__title")
            if not title_element:
                return None
            
            title = title_element.get_text(strip=True)
            if not title:
                return None
            
            player_element = item.select_one('div[data-test-id="audio-player"]')
            if not player_element:
                return None
            
            mp3_url = player_element.get("data-audio-player-preview-url-value")
            if not mp3_url:
                return None
            
            if not mp3_url.startswith('http'):
                mp3_url = f"https://mixkit.co{mp3_url}"
            
            return {"title": title, "url": mp3_url}
            
        except Exception:
            return None

    def _download_single_track(self, track: Dict[str, str], instrument: str, index: int) -> bool:
        """Скачивает один трек."""
        safe_title = self._create_safe_filename(track["title"])
        filename = f"{instrument}_{index:02d}_{safe_title}.mp3"
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
            if file_size > 1024:
                print(f"Скачан: {filename} ({file_size} байт)")
                return True
            else:
                os.remove(filepath)
                print(f"Файл слишком маленький: {filename}")
                return False
                
        except requests.Timeout:
            print(f"Таймаут при скачивании: {filename}")
        except requests.RequestException as e:
            print(f"Ошибка сети при скачивании {filename}: {e}")
        except Exception as e:
            print(f"Ошибка при скачивании {filename}: {e}")
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        return False

    def _create_safe_filename(self, name: str) -> str:
        """Создает безопасное имя файла."""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '_', name)
        name = name.strip('_.')
        return name[:80] if name else "unknown_track"

    def get_downloaded_files_info(self) -> List[Dict[str, str]]:
        """Возвращает информацию о всех скачанных файлах."""
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