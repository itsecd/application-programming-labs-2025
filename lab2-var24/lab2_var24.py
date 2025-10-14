import csv
import random
import argparse
import requests
from bs4 import BeautifulSoup
from typing import List
import os
import re
import json


class FileIterator:
    """
    Итератор по списку путей к файла
    """
    def __init__(self, paths: List[str]) -> None:
        self.paths: List[str] = paths
        self.index: int = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self.index < len(self.paths):
            result: str = self.paths[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


def parse_args() -> argparse.Namespace:
    """
    Парсинг командной строки
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True, help='Папка для сохранения всех треков')
    parser.add_argument('--csv_path', required=True, help='Путь к выходному CSV-файлу')
    return parser.parse_args()


def csv_init(csv_path: str) -> None:
    """
    Создаёт CSV-файл с заголовком
    """
    csv_header: List[str] = ["genre", "abs_path", "real_path", "url"]
    with open(csv_path, 'w', encoding="utf-8", newline="") as file:
        writer: csv.writer = csv.writer(file)
        writer.writerow(csv_header)


def append_to_csv(csv_path: str, genre: str, abs_path: str, real_path: str, url: str) -> None:
    """
    Добавляет строку в CSV-файл
    """
    with open(csv_path, 'a', encoding="utf-8", newline="") as file:
        writer: csv.writer = csv.writer(file)
        writer.writerow([genre, abs_path, real_path, url])


def generate_url(genre: str) -> str:
    """
    Создаёт ссылку на страницу жанра в Mixkit
    """
    return f"https://mixkit.co/free-stock-music/{genre}/"


def get_html(url: str) -> str:
    """
    Получает HTML страницы
    """
    headers: dict = {'User-Agent': 'Mozilla/5.0'}
    resp: requests.Response = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def mp3_parse(html: str) -> List[str]:
    """
    Парсит JSON-LD скрипты и извлекает ссылки
    """
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    urls: List[str] = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data: dict = json.loads(script.string or '')
        except json.JSONDecodeError:
            continue
        js: str = json.dumps(data)
        found: List[str] = re.findall(r'https://assets\.mixkit\.co/[^\s"]+\.mp3', js)
        urls.extend(found)
    return list(dict.fromkeys(urls))


def random_urls(urls: List[str]) -> List[str]:
    """
    Выбирает случайное непустое подмножество ссылок
    """
    if not urls:
        return []
    n: int = random.randint(1, len(urls))
    return random.sample(urls, n)


def download_mp3(url: str, path: str) -> None:
    """
    Скачивает MP3-файл по URL
    """
    try:
        resp: requests.Response = requests.get(url, timeout=(5, 30), stream=True)
        resp.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")


def process_genre(genre: str, output_dir: str, csv_path: str) -> None:
    """
    Обрабатывает один жанры
    """
    print(f"Обрабатываем жанр: {genre}")
    html: str = get_html(generate_url(genre))
    print(f"HTML получен, длина: {len(html)} символов")

    urls: List[str] = mp3_parse(html)
    print(f"Найдено ссылок: {len(urls)}")
    if not urls:
        print("Ссылки не найдены!")
        return

    select_urls: List[str] = random_urls(urls)
    print(f"Выбрано для скачивания: {len(select_urls)} ссылок")

    iterator: FileIterator = FileIterator(select_urls)
    for url in iterator:
        filename: str = f"{genre}_{os.path.basename(url)}"
        abs_p: str = os.path.join(output_dir, filename)
        real_path: str = os.path.relpath(abs_p, start=output_dir)
        print(f"Скачиваем: {url}")
        download_mp3(url, abs_p)
        append_to_csv(csv_path, genre, abs_p, real_path, url)


def main() -> None:
    """
    Основная функция программы
    """
    args: argparse.Namespace = parse_args()
    csv_init(args.csv_path)
    os.makedirs(args.output_dir, exist_ok=True)

    genres: List[str] = ['country', 'funk', 'classical']
    for genre in genres:
        process_genre(genre, args.output_dir, args.csv_path)


if __name__ == '__main__':
    main()
