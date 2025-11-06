import os
import re
import csv
import argparse
import requests

from bs4 import BeautifulSoup
from typing import List, Dict, Iterator

from track_iterator import TrackIterator


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_page(url: str, timeout: int = 3) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def get_total_pages(url: str) -> int:
    """
    return page count:
        <a class="pagination__link" ... >1</a>
        <a class="pagination__link" ... >2</a>
        ...
    """
    html = fetch_page(url)
    if not html:
        return 1
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find("div", class_="pagination__wrapper")
    if not pagination:
        return 1
    pages = [int(a.get_text(strip=True))
             for a in pagination.find_all("a", class_="pagination__link")
             if a.get_text(strip=True).isdigit()]
    return max(pages, default=1)


def extract_tracks_from_html(html: str) -> List[Dict[str, str]]:
    """
    output:
        [
            {"title": "song name", "mp3_link": "https://..."},
            ...
        ]
    """
    soup = BeautifulSoup(html, "html.parser")

    # контейнер со всеми блоками песен на странице
    # div.item-grid__items > [div.item-grid__item, ...]
    container = soup.select_one("div.item-grid__items")
    if not container:
        return []

    tracks = []
    for item in container.select("div.item-grid__item"):
        title_tag = item.select_one("h2.item-grid-card__title")
        player_tag = item.select_one('div[data-test-id="audio-player"]')

        if title_tag and player_tag:
            mp3_link = player_tag.get("data-audio-player-preview-url-value")

            if mp3_link and mp3_link.startswith("http"):
                tracks.append({
                    "title": title_tag.get_text(strip=True),
                    "mp3_link": mp3_link,
                })

    return tracks


def fetch_tracks(url: str, num_tracks: int) -> List[Dict[str, str]]:
    """
        функция собирает песни со всех страниц для какого то инструмента (если это необходимо)
        то есть, она фетчит страницу, выгружает оттуда все дикты[name: ..., url: ...]
        if хватило песен до num_tracks? -> хватит
        else фетчим следующую страницу

    output:
        [
            {"title": "song name", "mp3_link": "https://..."},
            ...
        ]
    """
    tracks = []
    total_pages = get_total_pages(url)

    for page in range(1, total_pages + 1):
        print(f"→ Loading page: {page}/{total_pages}")
        html = fetch_page(url + f"?page={page}")
        if not html:
            continue

        page_tracks = extract_tracks_from_html(html)
        tracks.extend(page_tracks)

        if len(tracks) >= num_tracks:
            return tracks[:num_tracks]

    return tracks


def good_filename(name: str) -> str:
    name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", name)
    name = re.sub(r'_+', "_", name)
    name = name.strip("_")
    return name[:100]


def download_tracks(tracks: List[Dict[str, str]], dest_dir: str, csv_path: str):
    """
    функция принимает дикт из всех найденных урлов для скачивная песен и
    пытается их скачать, попутно составляю csv аннотацию
    """
    os.makedirs(dest_dir, exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "absolute_path", "relative_path"])
        writer.writeheader()

        for i, track in enumerate(tracks, start=1):
            safe_name = good_filename(track["title"])
            filename = f"{i:03d}_{safe_name}.mp3"
            file_path = os.path.join(dest_dir, filename)

            try:
                resp = requests.get(track["mp3_link"], headers=HEADERS, timeout=10)
                resp.raise_for_status()

                with open(file_path, "wb") as f:
                    f.write(resp.content)

                abs_path = os.path.abspath(file_path)
                rel_path = os.path.relpath(file_path, start=os.getcwd())

                writer.writerow({
                    "title": track["title"],
                    "absolute_path": abs_path,
                    "relative_path": rel_path
                })

                print(f"✅ save: {filename}")

            except Exception as e:
                print(f"❌ error: {track['title']}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Mixkit music downloader")
    parser.add_argument("--folder", required=True, help="path/to/folder/with/music")
    parser.add_argument("--csv", required=True, help="path/to/CSV/file/annotation")
    parser.add_argument("--limit", type=int, default=5, help="track count for each category")

    return parser.parse_args()


def collect_all_tracks(instruments: list[str], limit: int) -> list[dict[str, str]]:
    """
    Функция собирает треки для указанных инструментов с сайта Mixkit.
    
    :param instruments: список инструментов (например ["acoustic-guitar", "drums"])
    :param limit: максимальное количество треков на каждый инструмент
    :return: список словарей с полями {"title": ..., "mp3_link": ...}
    """
    all_tracks = []
    for instrument in instruments:
        print(f"\n🎵 Category: {instrument}")
        url = f"https://mixkit.co/free-stock-music/instrument/{instrument}/"
        tracks = fetch_tracks(url, limit)
        print(f"Tracks found: {len(tracks)}")
        all_tracks.extend(tracks)

    return all_tracks


def main():
    args = parse_args()

    instruments = ["acoustic-guitar", "drums", "piano"]

    all_tracks = collect_all_tracks(instruments, args.limit)
    download_tracks(all_tracks, args.folder, args.csv)

    #for path in TrackIterator(args.csv):
    #    print("-", path)

if __name__ == "__main__":
    main()

