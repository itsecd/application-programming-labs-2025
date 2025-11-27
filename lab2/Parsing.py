from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv

BASE_URL: str = "https://mixkit.co/free-stock-music/instrument/"

def fetch_audio_urls(instrument: str) -> list[str]:
    """
    Получить список URL аудиофайлов.

    Парсит страницу mixkit.co и извлекает ссылки на аудиофайлы.

    :param instrument: Название инструмента (например, 'harp').
    :return: Список URL аудиофайлов или пустой список при ошибке.
    """
    urls: list[str] = []
    url = f"{BASE_URL}{instrument}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса страницы для {instrument}: {e}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'lxml')

        main = soup.find('main')
        if not main:
            raise ValueError('Main block not found')

        ordering = main.find('div', class_='item-grid__ordering')
        if not ordering:
            raise ValueError('Ordering block not found')

        wrapper = ordering.find('div', class_='item-grid__wrapper')
        if not wrapper:
            raise ValueError('Wrapper block not found')

        items_block = wrapper.find('div', class_='item-grid__items')
        if not items_block:
            raise ValueError('Items block not found')

        all_audio = items_block.find_all('div', class_='item-grid__item')
        for audio in all_audio:
            card = audio.find(
                'div',
                class_='item-grid-card item-grid-card--show-meta'
            )
            if not card:
                continue

            audio_player = card.find('div', {'data-test-id': 'audio-player'})
            if not audio_player:
                continue

            audio_link = audio_player.get(
                'data-audio-player-preview-url-value'
            )
            if not audio_link:
                continue

            urls.append(audio_link.strip())

        return urls

    except (ValueError, AttributeError) as e:
        print(f"Ошибка парсинга страницы для {instrument}: {e}")
        return []

def download_audio_files(
    instrument: str,
    urls: list[str],
    count: int,
    script_dir: Path
) -> list[list[str]]:
    """
    Скачать аудиофайлы и создать записи аннотации.

    :param instrument: Название инструмента.
    :param urls: Список URL для скачивания.
    :param count: Количество файлов для скачивания.
    :param script_dir: Директория скрипта для сохранения файлов.
    :return: Список записей [filename, absolute_path, relative_path].
    """
    audio_number: int = 0
    data: list[list[str]] = []

    download_dir = script_dir / 'Downloads' / instrument
    download_dir.mkdir(parents=True, exist_ok=True)

    for i in range(count):
        try:
            response = requests.get(urls[i])
            response.raise_for_status()
            audio_bytes = response.content
        except requests.RequestException as e:
            print(f"Ошибка при загрузке {urls[i]}: {e}")
            continue

        filename = f"{instrument}.{audio_number}.mp3"
        out_path = download_dir / filename

        try:
            out_path.write_bytes(audio_bytes)

            abs_path = out_path.resolve()
            rel_path = out_path.relative_to(script_dir)

            data.append([filename, str(abs_path), str(rel_path)])
            print(f"Аудио {filename} успешно скачано в {download_dir}!")

        except OSError as e:
            print(f"Ошибка записи файла {out_path}: {e}")
            continue

        audio_number += 1

    print(f"Все аудио обработаны для инструмента '{instrument}'")
    return data

def save_annotation(
    data: list[list[str]],
    csv_path: Path
) -> None:
    """
    Сохранить аннотацию в CSV-файл.

    :param data: Список записей [filename, absolute_path, relative_path].
    :param csv_path: Путь для сохранения CSV-файла.
    :raises IOError: При ошибке записи файла.
    """
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Absolute Path', 'Relative Path'])
            writer.writerows(data)
        print(f"CSV файл успешно создан: {csv_path}")
    except IOError as e:
        print(f"Ошибка при сохранении CSV: {e}")
        raise

