import csv
import random
import argparse
import requests
from bs4 import BeautifulSoup
from typing import List



CSV_HEADER = ["genre", "abs_path", "real_path", "url", ]

def csv_init(csv_path) -> None:
    """
    Создаёт CSV-файл с заголовком
    """

    with open(csv_path, 'w', encoding= "utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)


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
        

def mp3_parse(html) -> List[str]:
    """
    получаю ссылки на скачивание песни
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for tag in soup.select('a[href$=".mp3"]'):
        urls.append(tag['href'])
    return urls



def random_urls(urls) -> List[str]:
    """
    получаю n случайных ссылок на скачивание
    """
    n = random.randint(1, len(urls))
    return random.sample(urls, n)

def download_mp3(urls, path) -> None:
    resp = requests.get(url)
    resp.raise_for_status()
    with open(dest_path, 'wb') as file:
        file.write(resp.content)

