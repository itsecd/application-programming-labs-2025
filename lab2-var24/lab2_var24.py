import argparse
import csv
import json
import os
import random
import re
import requests
from typing import List


from bs4 import BeautifulSoup
class FileIterator:
    def __init__(self, dir_path: str) -> None:
        self.dir_path = os.path.abspath(dir_path)
        self.file_list = [os.path.join(self.dir_path, f) for f in os.listdir(self.dir_path)]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        while self.index < len(self.file_list):
            file_path = self.file_list[self.index]
            self.index += 1
            if file_path.lower().endswith('.mp3'):
                return file_path
        raise StopIteration


def parse_args() -> argparse.Namespace:
    """
    Парсинг командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', help='Папка для сохранения всех треков')
    parser.add_argument('--csv_path',  help='Путь к выходному CSV-файлу')
    return parser.parse_args()


def csv_init(csv_path: str) -> None:
    """
    Создаёт CSV-файл с заголовком
    """
    csv_header = ["genre", "abs_path", "real_path", "url"]
    with open(csv_path, 'w', encoding="utf-8", newline="") as file:
        writer: csv.writer = csv.writer(file)
        writer.writerow(csv_header)


def append_to_csv(csv_path: str, csv_data: List[str]) -> None:
    """
    Добавляет строку в CSV-файл
    """
    
    for data in csv_data:
        genre, abs_path, real_path, url = data
    
        with open(csv_path, 'a', encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
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
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def mp3_parse(html: str) -> List[str]:
    """
    Парсит JSON-LD скрипты и извлекает ссылки
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '') 
        except json.JSONDecodeError:
            continue
        js= json.dumps(data)
        found = re.findall(r'https://assets\.mixkit\.co/[^\s"]+\.mp3', js)
        urls.extend(found)
    return list(dict.fromkeys(urls))


def random_urls(urls: List[str]) -> List[str]:
    """
    Выбирает случайное непустое подмножество ссылок
    """
    if not urls:
        return []
    n = random.randint(1, len(urls))
    return random.sample(urls, n)


def download_mp3(url: str, path: str) -> None:
    """
    Скачивает MP3-файл по URL
    """
    try:
        resp = requests.get(url, timeout=(5, 30), stream=True)
        resp.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
    except Exception:
        raise


def process_genre(genre: str, output_dir: str, csv_path: str) -> None:
    """
    Обрабатывает один жанры
    """
    print(f"Обрабатываем жанр: {genre}")
    html = get_html(generate_url(genre))


    urls: List[str] = mp3_parse(html)
    print(f"Найдено ссылок: {len(urls)}")
    if not urls:
        print("Ссылки не найдены!")
        return      

    selected_urls: List[str] = random_urls(urls)
    print(f"Выбрано для скачивания: {len(selected_urls)} ссылок")

    
    csv_data: List[str] = []
    
    for url in selected_urls:
        
        filename = f"{genre}_{os.path.basename(url)}"
            
        print(f"Скачиваем: {url}")
        download_mp3(url, os.path.join(output_dir, filename))
            
    abs_path_iterator = FileIterator(output_dir)
        
    for abs_path in abs_path_iterator:
        real_path = os.path.join(output_dir, f"{genre}_{os.path.basename(url)}")
        csv_data.append([genre, abs_path, real_path, url])
          
    append_to_csv(csv_path,csv_data)


def main() -> None:
    """
    Основная функция программы
    """
    try:
        args = parse_args()
        csv_init(args.csv_path)
        os.makedirs(args.output_dir, exist_ok=True)

        genres = ['country', 'funk', 'classical']
        for genre in genres:
            process_genre(genre, args.output_dir, args.csv_path)
            
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")

if __name__ == '__main__':
    main()
