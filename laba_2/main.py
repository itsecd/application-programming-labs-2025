import requests
import csv
from bs4 import BeautifulSoup
import re
import time
from requests.auth import HTTPProxyAuth
import argparse
from typing import Tuple, List, Dict, Iterator, Union
import os

URL_BASE = 'https://mixkit.co/free-stock-music/instrument/piano/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

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
            with open(self.source, 'r', encoding='utf-8') as f:
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
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str,
                        help='Путь к папке для загрузки музыки')
    parser.add_argument('output_file', type=str,
                        help='Путь к CSV-файлу для сохранения результата')
    return parser.parse_args().source, parser.parse_args().output_file

def get_total_pages() -> int:
    resp = requests.get(URL_BASE, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    pagination = soup.find('div', class_='pagination__wrapper')
    if not pagination:
        return 1
    pages = [int(a.get_text(strip=True))
             for a in pagination.find_all('a', class_='pagination__link')
             if a.get_text(strip=True).isdigit()]
    return max(pages, default=1)

def parser_with_pagination(source: str, csv_path: str):
    os.makedirs(source, exist_ok=True)
    new_file = not os.path.exists(csv_path)
    csv_file = open(csv_path, 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=['text', 'link'])
    if new_file:
        writer.writeheader()

    total_pages = get_total_pages()
    print(f'Всего страниц: {total_pages}')

    for page in range(1, total_pages + 1):
        resp = requests.get(URL_BASE, headers=HEADERS, params={'page': page})
        if resp.status_code != 200:
            print(f'Страница {page}: ошибка {resp.status_code}')
            continue

        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('div.item-grid__item')
        print(f'Парсинг страницы {page}: найдено {len(items)} треков')

        for item in items:
            title_tag = item.select_one('h2.item-grid-card__title')
            player = item.select_one('div[data-test-id="audio-player"]')
            if not title_tag or not player:
                continue

            name = title_tag.get_text(strip=True)
            link = player.get('data-audio-player-preview-url-value')
            try:
                r = requests.get(link, headers=HEADERS, timeout=10)
                r.raise_for_status()
                safe = re.sub(r'[<>:"/\\|?*]', '_', name)[:100]
                filename = f"page{page}_{safe}.mp3"
                path = os.path.join(source, filename)
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"Скачан: {path}")
                writer.writerow({'text': name, 'link': link})
                csv_file.flush()

            except Exception as e:
                print(f"Ошибка скачивания {name}: {e}")

        time.sleep(1)
    csv_file.close()

if __name__ == '__main__':
    src, out_csv = parser_t()
    parser_with_pagination(src, out_csv)
    print("Список скачанных файлов:")
    for filepath in FilePathIterator(src):
        print(filepath)