import csv
import random
import argparse
import requests
from bs4 import BeautifulSoup
from typing import List
import os
import re
import json



def parse_args() -> argparse.Namespace:
    """
    парсинг командной строки
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--output_dir',required=True,help='Папка для сохранения всех треков')
    parser.add_argument( '--csv_path',required=True,help='Путь к выходному CSV-файлу')
    return parser.parse_args()


def csv_init(csv_path) -> None:
    """
    Создаёт CSV-файл с заголовком
    """
    csv_header = ["genre", "abs_path", "real_path", "url"]

    with open(csv_path, 'w', encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)


def append_to_csv(csv_path, genre, abs_path, real_path, url) -> None:
    """
    добавляет строки  в CSV-файл
    """

    with open(csv_path, 'a', encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([genre, abs_path, real_path, url])

def generate_url(genre) -> str:
    """
    создаю ссылку на страницу жанра в mixkit
    """
    return f"https://mixkit.co/free-stock-music/{genre}/"

def get_html(url) -> str:
    """
    получаю страницу
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    resp = requests.get(url, headers= headers)
    if resp.ok:
        return resp.text
        

def mp3_parse(html: str) -> List[str]:
    """
    Парсит JSON-LD скрипты и извлекает mp3-ссылки.
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []

    
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '')
        except json.JSONDecodeError:
            continue
        
        js = json.dumps(data)
        
        found = re.findall(r'https://assets\.mixkit\.co/[^\s"]+\.mp3', js)
        urls.extend(found)

    
    return list(dict.fromkeys(urls))




def random_urls(urls) -> List[str]:
    """
    получаю n случайных ссылок на скачивание
    """
    if not urls:
        
        return []

    n = random.randint(1, len(urls))
    return random.sample(urls, n)


def download_mp3(url, path):
    try:
        resp = requests.get(url, timeout=10)
        print(f"[{url}] Status: {resp.status_code}, Content-Length: {resp.headers.get('Content-Length')}")
        resp.raise_for_status()
        with open(path, 'wb') as f:
            f.write(resp.content)
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")



def process_genre(genre, output_dir, csv_path) -> None:
    print(f"Обрабатываем жанр: {genre}")
    html = get_html(generate_url(genre))
    print(f"HTML получен, длина: {len(html)} символов")
    
    urls = mp3_parse(html)
    print(f"Найдено ссылок: {len(urls)}")
    
    if not urls:
        print("Ссылки не найдены!")
        return
        
    select_urls = random_urls(urls)
    print(f"Выбрано для скачивания: {len(select_urls)} ссылок")
    
    for url in select_urls:
        filename = os.path.basename(url)
        real = filename
        abs_p = os.path.join(output_dir, real)
        print(f"Скачиваем: {url}")
        download_mp3(url, abs_p)
        append_to_csv(csv_path, genre, abs_p, real, url)




def main() -> None:
    """
    основная функция программы
    """ 

    


    genres = ['country', 'funk', 'classical']

    args = parse_args()
    csv_init(args.csv_path)
    os.makedirs(args.output_dir, exist_ok=True)
    for genre in genres:
        process_genre(genre, args.output_dir, args.csv_path)
    

if __name__ == '__main__':
    main()