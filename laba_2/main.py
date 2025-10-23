import argparse
import re
import time
from typing import Tuple, List, Dict, Iterator, Union
import os

from bs4 import BeautifulSoup
import csv
import requests

URL_BASE = "https://mixkit.co/free-stock-music/instrument/piano/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

MAX_FILENAME_LENGTH = 100


def sanitize_filename(name: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
    """
    Очищает строку name от запрещённых символов в файловой системе
    и усечёт до max_length символов.
    """
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name)
    return cleaned[:max_length]


class FilePathIterator(Iterator[str]):
    def __init__(self, source: Union[str, os.PathLike]):
        """
        source: путь к папке или к файлу, где каждая строка — путь к файлу.
        """
        self.source = str(source)
        self._paths = []
        self._index = 0

        if os.path.isdir(self.source):
            self._paths = [
                os.path.join(self.source, fn)
                for fn in os.listdir(self.source)
                if os.path.isfile(os.path.join(self.source, fn))
            ]
        elif os.path.isfile(self.source):
            with open(self.source, "r", encoding="utf-8") as f:
                self._paths = [line.strip() for line in f if line.strip()]
        else:
            raise ValueError(f"Неправильный источник: {self.source}")

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._paths):
            raise StopIteration
        path = self._paths[self._index]
        self._index += 1
        return path


def parser_t() -> Tuple[str, str]:
    """
    Позволяет через консоль запускать код с аргументами
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Путь к папке для загрузки музыки")
    parser.add_argument(
        "output_file", type=str, help="Путь к CSV-файлу для сохранения результата"
    )
    parser.add_argument("-m", "--mode", type=str, help="Режим работы с файлом")
    args = parser.parse_args()
    return args.source, args.output_file, args.mode


def get_total_pages() -> int:
    """
    Реализует подсчет страниц
    """
    resp = requests.get(URL_BASE, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    pagination = soup.find("div", class_="pagination__wrapper")
    if not pagination:
        return 1
    pages = [
        int(a.get_text(strip=True))
        for a in pagination.find_all("a", class_="pagination__link")
        if a.get_text(strip=True).isdigit()
    ]
    return max(pages, default=1)


def extract_tracks_from_page(page_num: int) -> List[Dict[str, str]]:
    """
    Получает список треков со страницы:
    возвращает [{'name': ..., 'link': ...}, ...]
    """
    resp = requests.get(
        URL_BASE, headers=HEADERS, params={"page": page_num}, timeout=10
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("div.item-grid__item")

    tracks = []
    for item in items:
        title = item.select_one("h2.item-grid-card__title")
        player = item.select_one('div[data-test-id="audio-player"]')
        if not title or not player:
            continue
        name = title.get_text(strip=True)
        link = player.get("data-audio-player-preview-url-value")
        if name and link and link.startswith("http"):
            tracks.append({"name": name, "link": link})
    return tracks


def download_single_track(track: Dict[str, str], dest_dir: str, page_num: int) -> str:
    """
    Скачивает один трек по track['link'] и сохраняет в dest_dir.
    """
    name = track["name"]
    link = track["link"]
    resp = requests.get(link, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    safe_name = sanitize_filename(name)
    filename = f"page{page_num}_{safe_name}.mp3"
    path = os.path.join(dest_dir, filename)

    with open(path, "wb") as f:
        f.write(resp.content)
    print(f"Скачан: {path}")

    return path


def get_corrent_mode(mode: str):
    """
    Проверяет валидность режима работы
    """
    if mode in ["append", "a"]:
        return "a"
    return "w"


def get_corrent_csv_path(csv_path: str):
    """
    Проверяет существует ли .csv в пути/названии или нет
    """
    match = re.search(".csv$", csv_path)
    if match:
        return
    return csv_path + ".csv"


def parser_with_pagination(source: str, csv_path: str, mode: str) -> None:
    """Главная функция: координирует парсинг и скачивание."""
    os.makedirs(source, exist_ok=True)

    with open(csv_path, mode, encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["text", "absolute_path", "relative_path"]
        )

        is_file_exists = os.path.exists(csv_path)
        if mode != 'a' or not is_file_exists:
            writer.writeheader()

        total_pages = get_total_pages()
        print(f"Всего страниц: {total_pages}")

        for page in range(1, total_pages + 1):
            tracks = extract_tracks_from_page(page)
            print(f"Страница {page}: найдено {len(tracks)} треков")

            for track in tracks:
                try:
                    local_path = download_single_track(track, source, page)

                    abs_path = os.path.abspath(local_path)
                    rel_path = os.path.relpath(local_path, start=source)

                    writer.writerow(
                        {
                            "text": track["name"],
                            "absolute_path": abs_path,
                            "relative_path": rel_path,
                        }
                    )
                    csv_file.flush()
                except Exception as e:
                    print(f"Ошибка скачивания {track['name']}: {e}")

            time.sleep(1)


def main():
    src, out_csv, mode = parser_t()
    out_csv = get_corrent_csv_path(out_csv)
    mode = get_corrent_mode(mode)
    parser_with_pagination(src, out_csv, mode)
    print("Список скачанных файлов:")
    for filepath in FilePathIterator(src):
        print(filepath)


if __name__ == "__main__":
    main()
