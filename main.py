import requests
from bs4 import BeautifulSoup
import csv
import os

def parse_music_data(music_type: str) -> list[dict[str, str | None]]:
    """
    Выполняет запрос на сайт mixkit.co; считывает со страницы информацию о всех музыкальных композициях
    Args:
        music_type (str): определяет тэг по которому происходит поиск
    Returns:
        tracks (list): Данные о композициях и ссылка на скачивание
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    response = requests.get(f"https://mixkit.co/free-stock-music/instrument/{music_type}/", headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Все музыкальные композиции хранятся в элементах этого html класса \/
    data_elements = soup.find_all("div", class_="item-grid-card item-grid-card--show-meta")
    tracks = list()
    for element in data_elements:
        track = {
            "name": element.find_next("h2").text.rstrip().lstrip(),
            "author": element.find_next("p").text.rstrip().lstrip(),
            "duration": element.find("div", {"data-test-id": "duration"}, recursive=True).text.rstrip().lstrip(),
            "link": element.find("div", attrs={"data-audio-player-preview-url-value": True}).get("data-audio-player-preview-url-value")
        }
        tracks.append(track)
    return tracks


def download_file(folder: str, url: str) -> None:
    """
    Скачивает файл, обращаясь за ним по url-запросу
    Args:
        folder (str): Папка, куда будут сохраняться файлы
        urls (str): URL-адрес файла 
    """
    ...


def main(downloads_folder: str, csv_path: str, amount: int) -> None:
    """ 
    Основная логика программы 
    Args:
        downloads_folder (str): Путь до папки загрузки
        csv_path (str): Файл для аннотаций на загруженные файлы
        amount (int): Кол-во загруженных файлов
    """
    flute_tracks = parse_music_data("flute")
    violin_tracks = parse_music_data("violin")
    drums_tracks = parse_music_data("drums")

    max_amount = len(flute_tracks) + len(violin_tracks) + len(drums_tracks)
    if amount > max_amount:
        print(f"Запрошено слишком много. Будет сохранено: {max_amount}")
        amount = max_amount


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, help="Путь для каталога вывода.", default="")
    parser.add_argument("-c", "--csv", type=str, help="Путь к файлу аннотации", default="annotation.csv")
    parser.add_argument("-a", "--amount", type=int, help="Количество файлов для парсинга", default=64)
    args = parser.parse_args()

    try:
        if args.amount > 1:
            main(args.output, args.csv, args.amount)
        else:
            raise ValueError("Значение --amount должно быть положительным!")
    except ValueError as e:
        print(f"Ошибка параметра: {e}")
    except FileNotFoundError as e:
        print(f'Ошибка, не найден файл: "{e.filename}"')
    except PermissionError as e:
        print(f"Недостаточно прав для совершения операции: {e}")
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
