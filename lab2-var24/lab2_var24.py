import csv
import random
import argparse
import requests
from bs4 import BeautifulSoup


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
        
