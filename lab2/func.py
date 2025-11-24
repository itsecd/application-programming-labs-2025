import argparse
import csv
import os
import random
import requests
from bs4 import BeautifulSoup
from iter import SoundtrackIterator

def get_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, default="downloads")
    parser.add_argument("-c", "--csv", type=str, default="downloads/ann.csv")
    parser.add_argument("-n", "--number", type=int, default=50)
    return parser.parse_args()

def collect_tracks(genre: str) -> list[dict[str, str]]:
    """
    Извлекает информацию о треках с сайта mixkit.co
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }

    if genre == "R&B":
        url_genre = "r&b"
    else:
        url_genre = genre
    
    url = f"https://mixkit.co/free-stock-music/{url_genre}/"
    response = requests.get(url, headers=headers, timeout=40)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="item-grid-card item-grid-card--show-meta")

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

def download_audio_track(gen_fol: str, url: str) -> str:
    """Скачивает аудиофайл в папку жанра"""
    os.makedirs(gen_fol, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(gen_fol, filename)

    if not os.path.exists(filepath):
        with requests.get(url, stream=True, timeout=40) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for data_part in response.iter_content(8192):
                    f.write(data_part)
    return filename

def handle_genre(genre: str, base_dir: str, writer: csv.writer, tracks_per_genre: int) -> int:
    """Обрабатывает один жанр: парсит, скачивает треки и записывает в CSV"""
    print(f"Обработка жанра: {genre}")
    try:
        all_tracks = collect_tracks(genre)
    except requests.RequestException as e:
        print(f"Ошибка при запросе ({genre}): {e}")
        return 0

    if not all_tracks:
        print(f"Нет доступных треков для жанра: {genre}")
        return 0

    count = min(tracks_per_genre, len(all_tracks))
    selected = random.sample(all_tracks, count)

    print(f"Будут скачаны {count} треков жанра '{genre}'.")
    genre_dir = os.path.join(base_dir, genre)
    downloaded_count = 0

    for track in selected:
        try:
            fname = download_audio_track(genre_dir, track["link"])
            rel_path = f"{genre}/{fname}"
            abs_path = os.path.abspath(os.path.join(genre_dir, fname))
            writer.writerow([rel_path, abs_path, genre, track["title"], track["artist"]])
            downloaded_count += 1
        except requests.RequestException as e:
            print(f"Ошибка загрузки '{track['title']}': {e}")
    return downloaded_count

def run_downloads(out_dir: str, csv_file: str, genres: list[str]) -> dict[str, int]:
    """Организует загрузку треков по всем жанрам и формирует CSV-аннотацию"""

    args = get_args()
    total_tracks = max(50, min(1000, args.number))
    
    tracks_per_genre = total_tracks // len(genres)
    print(f"Общее количество треков: {total_tracks}, по {tracks_per_genre} на каждый жанр")
    
    results = {"genres_processed": 0, "tracks_total": 0}
    
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Относительный путь", "Абсолютный путь", "Жанр", "Название", "Исполнитель"])

        for genre in genres:
            downloaded = handle_genre(genre, out_dir, writer, tracks_per_genre)
            if downloaded:
                results["genres_processed"] += 1
                results["tracks_total"] += downloaded

    return results

def print_summary(csv_file: str, stats: dict[str, int]) -> None:
    """Вывод статистики и предпросмотра содержимого CSV."""
    print(f"Завершено. Количество треков: {stats['tracks_total']}")
    print("Предпросмотр аннотации:")
    
    for row in SoundtrackIterator(csv_file):
        print(row)