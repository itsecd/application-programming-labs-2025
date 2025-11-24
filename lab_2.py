import argparse
import csv
import os
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки
    """
    parser = argparse.ArgumentParser(description="Парсинг звуков с mixkit.co")
    parser.add_argument('download_dir', type=str, help='Папка для сохранения аудиофайлов')
    parser.add_argument('annotation', type=str, help='Путь к CSV-файлу с аннотацией')
    return parser.parse_args()


def time_to_seconds(time_str: str) -> int:
    """
    Преобразует '0:12' или '1:30' в секунды
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 1:
            return int(parts[0])
    except (ValueError, AttributeError):
        pass
    return 0


def parse_mixkit_sound_page(url: str) -> list[list[str]]:
    """
    Парсит сайт и возвращает список списков в которых название, ссылка и длительность
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('div.item-grid__item')
    results = []
    for item in items:
        title_elem = item.select_one('h2.item-grid-card__title')
        title = title_elem.get_text(strip=True) if title_elem else "Unknown"

        audio_div = item.find('div', attrs={'data-audio-player-preview-url-value': True})
        audio_url = audio_div.get('data-audio-player-preview-url-value') if audio_div else None

        time_elem = item.select_one('div.item-grid-sfx-preview__meta-time')
        duration = time_elem.get_text(strip=True) if time_elem else "0:00"

        if not audio_url:
            continue

        audio_url = urljoin("https://mixkit.co", audio_url)
        results.append([title, audio_url, duration])
    return results


def download_sound(url: str, folder: str, filename: str) -> str:
    """
    Скачивает звук и возвращает абсолютный путь к файлу
    """
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return os.path.abspath(filepath)
    except Exception as e:
        print(f"Не удалось скачать {url}: {e}")
    return ""

class SoundPathIterator:
    """
    Итератор по абсолютным путям к аудиофайлам из CSV-аннотации
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._file = None
        self._reader = None

    def __iter__(self):
        self._file = open(self.csv_path, mode='r', encoding='utf-8', newline='')
        self._reader = csv.reader(self._file)
        next(self._reader, None)
        return self

    def __next__(self):
        try:
            row = next(self._reader)
            if len(row) >= 2:
                return row[1]
            else:
                raise StopIteration
        except StopIteration:
            if self._file:
                self._file.close()
            raise
            
def save_sounds_and_create_annotation(all_sounds: list, download_dir: str, annotation_path: str) -> None:
    """
    Скачивает звуки из списка и создаёт CSV-аннотацию с относительными и абсолютными путями.

    :param all_sounds: Список звуков в формате [(title, audio_url, duration), ...]
    :param download_dir: Папка для сохранения аудиофайлов
    :param annotation_path: Путь к выходному CSV-файлу
    """
    with open(annotation_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['relative_path', 'absolute_path'])

        for i, (title, audio_url, duration) in enumerate(all_sounds):
            filename = f"sound_{i+1:04d}.mp3"
            abs_path = download_sound(audio_url, download_dir, filename)
            if abs_path:
                rel_path = os.path.relpath(abs_path, start=os.getcwd())
                writer.writerow([rel_path, abs_path])
            time.sleep(0.3)

def main():
    args = parse_arguments()
    download_dir = args.download_dir
    annotation_path = args.annotation
    os.makedirs(download_dir, exist_ok=True)

    base = 'https://mixkit.co/free-sound-effects'
    themes = [
        '/transition', '/nature', '/technology', '/funny', '/notification',
        '/animals', '/transport', '/human', '/warfare', '/instrument',
        '/lifestyle', '/game', '/misc'
    ]
    urls_to_parse = [base] + [base + theme for theme in themes]

    all_sounds = []
    MIN_DURATION_SEC = 10
    MAX_FILES = 1000
    MIN_FILES = 50

    print("Сбор звуков длиной более 10 секунд...")

    for url in urls_to_parse:
        if len(all_sounds) >= MAX_FILES:
            break
        print(f"Парсинг: {url}")
        for page in range(1, 4):
            if len(all_sounds) >= MAX_FILES:
                break
            page_url = f"{url}?page={page}" if page > 1 else url
            sounds = parse_mixkit_sound_page(page_url)
            if not sounds:
                break

            for title, audio_url, duration_str in sounds:
                duration_sec = time_to_seconds(duration_str)
                if duration_sec > MIN_DURATION_SEC:
                    all_sounds.append([title, audio_url, duration_str])
                    if len(all_sounds) >= MAX_FILES:
                        break
                      
            time.sleep(0.8)
    if len(all_sounds) < MIN_FILES:
        print(f"Найдено только {len(all_sounds)} звуков (минимум {MIN_FILES} по ТЗ).")
        if len(all_sounds) == 0:
            print("Нет подходящих звуков. Завершение.")
            return
    else:
        all_sounds = all_sounds[:MAX_FILES]
    print(f"Найдено {len(all_sounds)} подходящих звуков. Начинаем скачивание...")
    save_sounds_and_create_annotation(all_sounds, download_dir, annotation_path)
    print(f"Готово! Скачано {len(all_sounds)} звуков. Аннотация: {annotation_path}")
    print("\nПример итерации по файлам:")
    count = 0
    for path in SoundPathIterator(annotation_path):
        print(f"  {path}")
        count += 1
        if count >= 3:
            break
    if count == 0:
        print("  Нет файлов для итерации.")

if __name__ == '__main__':
    main()
