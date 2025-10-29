import requests
from bs4 import BeautifulSoup
import csv
import os
import argparse
from typing import List, Iterator

class FileIterator:
    """
    Итератор
    """
    def __init__(self, paths: List[str]) -> None:
        self.paths = paths
        self.index = 0

    def __iter__(self) -> Iterator[str]:
        return self
    
    def __next__(self) -> str:
        if self.index < len(self.paths):
            item = self.paths[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration
    

def csv_init(csv_path: str) -> None:
    """
    Создает новый CSV-файл с заголовками.
    Параметры:
        csv_path (str): путь к CSV-файлу.
    """
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["abs_path", "rel_path", "url"])

def append_to_csv(csv_path: str, abs_path: str, rel_path: str, url: str) -> None:
    """
    Добавляет одну строку в CSV-файл с данными о скачанном файле.
    Параметры:
        csv_path (str): путь к CSV-файлу.
        abs_path (str): абсолютный путь к файлу.
        rel_path (str): относительный путь к файлу.
        url (str): ссылка на источник файла.
    """
    with open(csv_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([abs_path,rel_path,url])


def get_html(url: str) -> str:
    """
    Загружает HTML-код страницы по указанному URL.
    Параметры:
        url (str): адрес веб-страницы.

    Возвращает:
        str: текст HTML-документа.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    return resp.text


def mp3_parse(html: str) -> List[str]:
    """
    Парсит HTML и извлекает все ссылки на mp3-файлы.
    Параметры:
        html (str): HTML-код страницы.

    Возвращает:
        List[str]: список URL-адресов mp3-файлов.
    """
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for div in soup.find_all("div", attrs={"data-audio-player-preview-url-value": True}):
        urls.append(div["data-audio-player-preview-url-value"])
    return list(dict.fromkeys(urls))

def download_mp3(url: str, path: str) -> None:
    """
    Скачивает mp3-файл по указанному URL и сохраняет его на диск.
    Параметры:
        url (str): ссылка на mp3-файл.
        path (str): путь для сохранения файла.
    """
    try:
        r = requests.get(url, stream = True)
        with open(path, "wb") as file:
            for chunk in r.iter_content(8192):
                if chunk:
                    file.write(chunk)
    except Exception as error:
        print("Ошибка при загрузке:", url, error)


def process_transport(output_dir: str, csv_path: str) -> None:
    """
    Загружает и сохраняет звуки категории 'Transport'.

    Параметры:
        output_dir (str): папка для сохранения mp3-файлов.
        csv_path (str): путь к создаваемому CSV-файлу
    """
    url = "https://mixkit.co/free-sound-effects/transport/"
    print("Загрузка данных с сайта:", url)
    html = get_html(url)
    urls = mp3_parse(html)
    print("Найдено файлов .mp3", len(urls))

    if not urls:
        print("Файлы не найдены")
        return 
    
    os.makedirs(output_dir, exist_ok=True)
    csv_init(csv_path)

    iterator = FileIterator(urls)

    for u in iterator:
        name = os.path.basename(u)
        abs_p = os.path.join(output_dir, name)
        rel_p = os.path.relpath(abs_p, start=output_dir)
        print("Загрузка:", name)
        download_mp3(u, abs_p)
        append_to_csv(csv_path, abs_p, rel_p, u)
    
    print("Завершено! CSV-файл сохранён по пути", csv_path)

def main():
    """
    Точка входа программы. 
    Обрабатывает аргументы командной строки и запускает основную функцию.
    
    Аргументы командной строки:
        --output_dir : каталог для сохранения файлов.
        --csv_path   : путь к файлу аннотации (CSV).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", required=True, help="Папка для сохранения mp3-файлов")
    parser.add_argument("--csv_path", required=True, help="Путь к CSV-файлу аннотации")
    args = parser.parse_args()

    process_transport(args.output_dir, args.csv_path)


if __name__ == "__main__":
    main()