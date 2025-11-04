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

MAX_FILENAME_LENGTH = 50

def args_parse() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        prog="Data parser", description="Parsing data from file"
    )
    parser.add_argument("-f", "--file", type=str, help="file for csv")
    parser.add_argument("-o", "--output", type=str, help="Output file for downloads music")

    return parser.parse_args()




def sanitize_filename(name: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
    """
    Очищает строку name от запрещённых символов в файловой системе
    и усечёт до max_length символов.
    """
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name)
    return cleaned[:max_length]


def extrackt_tracks_from_page(page_num: int) -> List[Dict[str, str]]:
    """
    Получает список треков со страницы:
    возвращает список {'name': ..., 'link': ...}
    """
    resp = requests.get(
        URL_BASE, headers=HEADERS, params={"page": page_num}, timeout=10
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("div.item-grid__item")
    music=[]
    for item in items:
        name=item.select_one("h2.item-grid-card__title").get_text(strip=True)
        link = item.select_one('div[data-audio-player-preview-url-value]').get('data-audio-player-preview-url-value')
        if name and link and link.startswith("http"):
            music.append({"name": name, "link": link})
    return music

def download_single_track(music: Dict[str, str], dir: str, page_num: int) -> str:
    """
    Скачивает один трек по music['link'] и сохраняет в dir.
    """
    name = music["name"]
    link = music["link"]
    resp = requests.get(link, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    safe_name = sanitize_filename(name)
    filename = f"page{page_num}_{safe_name}.mp3"
    path = os.path.join(dir, filename)

    with open(path, "wb") as f:
        f.write(resp.content)
    print(f"Скачан: {path}")

    return path

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

def get_corrent_csv_path(csv_path: str):
    """
    Проверяет существует ли .csv в пути/названии или нет
    """
    match = re.search(".csv$", csv_path)
    if match:
        return
    return csv_path + ".csv"

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

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._paths):
            raise StopIteration
        path = self._paths[self._index]
        self._index += 1
        return path

def parser_with_pagination(source: str, csv_path: str) -> None:
    """"Главная функция скачивания"""
    os.makedirs(source, exist_ok=True)
    
    with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["name", "absolute_path", "relative_path"]
        )
        writer.writeheader()  
        
        total_pages = get_total_pages()
        
        for page in range(1, total_pages + 1):
            tracks = extrackt_tracks_from_page(page)
            
            for track in tracks:
                try:
                    local_path = download_single_track(track, source, page)

                    abs_path = os.path.abspath(local_path)
                    rel_path = os.path.relpath(local_path, start=source)

                    writer.writerow({
                        "name": track["name"],
                        "absolute_path": abs_path,
                        "relative_path": rel_path,
                    })
                    csv_file.flush()  
                except Exception as e:
                    print(f"Ошибка скачивания {track['name']}: {e}")
            
            time.sleep(1) 
    

def main():
    args = args_parse()

    if not args.output:
        print("Please specify output directory using -o argument")
        return
    
    if not args.file:
        print("Please specify file directory using -f argument")
        return
    
    print(f"Starting to download songs to {args.output}")
    
    out_csv=get_corrent_csv_path(args.file)
    parser_with_pagination(args.output, out_csv)
    for filepath in FilePathIterator(args.output):
        print(filepath)


if __name__ == "__main__":
    main()
    

