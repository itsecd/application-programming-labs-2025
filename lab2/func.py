import argparse
import csv
import os
import random
import requests

from bs4 import BeautifulSoup
from itr import SoundtrackIterator


def get_args() -> argparse.Namespace:
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Парсинг и загрузка случайных аудиотреков с mixkit.co по жанрам.")
    parser.add_argument("-o", "--output", type=str, default="downloads", help="Папка для загрузок")
    parser.add_argument("-c", "--csv", type=str, default="downloads/annotation.csv", help="CSV-файл аннотаций")
    return parser.parse_args()


def collect_tracks(genre: str) -> list[dict[str, str]]:
    """
    Извлекает данные о треках указанного жанра с сайта mixkit.co.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }

    url = f"https://mixkit.co/free-stock-music/{genre}/"
    response = requests.get(url, headers=headers, timeout=40)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("div.item-grid-card.item-grid-card--show-meta")

    tracks = []
    for card in cards:
        name_tag = card.find("h2")
        author_tag = card.find("p")
        audio_tag = card.find("div", attrs={"data-audio-player-preview-url-value": True})
        if not (name_tag and author_tag and audio_tag):
            continue
        tracks.append({
            "title": name_tag.get_text(strip=True),
            "artist": author_tag.get_text(strip=True).replace("by ", ""),
            "link": audio_tag["data-audio-player-preview-url-value"],
        })
    return tracks


def save_audio_file(genre_folder: str, url: str) -> str:
    """
    Скачивает трек по ссылке и сохраняет в указанную директорию.
    """
    os.makedirs(genre_folder, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(genre_folder, filename)

    if not os.path.exists(filepath):
        with requests.get(url, stream=True, timeout=40) as resp:
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
    return filename


def handle_genre(genre: str, base_dir: str, writer: csv.writer) -> int:
    """Обрабатывает жанр: выбирает случайные треки, скачивает и записывает в CSV."""
    print(f"\nОбработка жанра: {genre}")
    try:
        all_tracks = collect_tracks(genre)
    except requests.RequestException as e:
        print(f"Ошибка при запросе ({genre}): {e}")
        return 0

    if not all_tracks:
        print(f"Нет доступных треков для жанра: {genre}")
        return 0

    count = random.randint(17, min(26, len(all_tracks)))  # Длина всех треков в жанре минимум 24
    selected = random.sample(all_tracks, count)

    print(f"Будут скачаны {count} треков жанра '{genre}'.")
    genre_dir = os.path.join(base_dir, genre)
    count = 0

    for track in selected:
        try:
            fname = save_audio_file(genre_dir, track["link"])
            rel_path = f"{genre}/{fname}"
            abs_path = os.path.abspath(os.path.join(genre_dir, fname))
            writer.writerow([rel_path, abs_path, genre.capitalize(), track["title"], track["artist"]])
            count += 1
        except requests.RequestException as e:
            print(f"Ошибка загрузки '{track['title']}': {e}")
    return count


def run_downloads(out_dir: str, csv_file: str, genres: list[str]) -> dict[str, int]:
    """
    Главная функция загрузки треков по жанрам и записи аннотации в CSV.
    """
    results = {"genres_processed": 0, "tracks_total": 0}
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Относительный путь", "Абсолютный путь", "Жанр", "Название", "Исполнитель"])

        for genre in genres:
            downloaded = handle_genre(genre, out_dir, writer)
            if downloaded:
                results["genres_processed"] += 1
                results["tracks_total"] += downloaded

    return results


def print_summary(csv_file: str, stats: dict[str, int]) -> None:
    """Вывод статистики и содержимого CSV."""
    print(f"\nЗавершено. Количество треков: {stats['tracks_total']}")
    print("\nПредпросмотр аннотации:\n")
    for row in SoundtrackIterator(csv_file):
        print(row)
