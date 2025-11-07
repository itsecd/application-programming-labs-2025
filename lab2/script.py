import os
import re
import csv
import argparse
import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Iterator

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_page(url: str, timeout: int = 10) -> str | None:
    """
    Загружает HTML страницу по указанному URL.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"❌ Ошибка загрузки страницы {url}: {e}")
        return None


def get_total_pages(url: str) -> int:
    """
    Определяет общее количество страниц с звуками животных.
    """
    html = fetch_page(url)
    if not html:
        return 1

    soup = BeautifulSoup(html, "html.parser")

    pagination = soup.find("div", class_="pagination__wrapper")
    if not pagination:
        pagination = soup.find("nav", class_="pagination")
    if not pagination:
        pagination = soup.find("ul", class_="pagination")

    if pagination:
        pages = [int(a.get_text(strip=True))
                 for a in pagination.find_all
                 ("a", class_=lambda x: x and "pagination" in x)
                 if a.get_text(strip=True).isdigit()]
        if pages:
            return max(pages)

    if 'page/2/' in html:
        return 2

    return 1


def extract_animal_sounds_from_html(html: str) -> List[Dict[str, str]]:
    """
    Извлекает информацию о звуках животных из HTML страницы.
    """
    soup = BeautifulSoup(html, "html.parser")
    sounds = []

    container = soup.select_one("div.item-grid__items")
    if not container:
        container = soup.select_one("div.grid-cards")
    if not container:
        container = soup.select_one("div.sounds-grid")

    if container:
        for item in container.select("div.item-grid__item,"
                                     " div.grid-card, div.sound-card"):
            title_tag = item.select_one(
                "h2.item-grid-card__title, h3.card-title, h4.sound-title")
            if not title_tag:
                continue

            mp3_link = None

            player_tag = item.select_one(
                'div[data-audio-player-preview-url-value]')
            if player_tag:
                mp3_link = player_tag.get(
                    "data-audio-player-preview-url-value")

            if not mp3_link:
                mp3_element = item.select_one('[data-mp3]')
                if mp3_element:
                    mp3_link = mp3_element.get("data-mp3")

            if not mp3_link:
                audio_tag = item.select_one("audio source[src$='.mp3']")
                if audio_tag:
                    mp3_link = audio_tag.get("src")

            if mp3_link and mp3_link.startswith("http"):
                sounds.append({
                    "title": title_tag.get_text(strip=True),
                    "mp3_link": mp3_link,
                })

    if not sounds:
        players = soup.find_all(
            attrs={"data-audio-player-preview-url-value": True})
        for player in players:
            title = player.get("title") or "Animal Sound"
            mp3_link = player.get("data-audio-player-preview-url-value")
            if mp3_link and mp3_link.startswith("http"):
                sounds.append({
                    "title": title,
                    "mp3_link": mp3_link,
                })

    return sounds


def fetch_animal_sounds(url: str, num_sounds: int) -> List[Dict[str, str]]:
    """
    Собирает звуки животных со всех доступных страниц.
    """
    sounds = []
    total_pages = get_total_pages(url)

    print(f"📄 Всего страниц для обработки: {total_pages}")

    for page in range(1, total_pages + 1):
        print(f"→ Загружаем страницу: {page}/{total_pages}")

        if page == 1:
            page_url = url
        else:
            page_url = f"{url}page/{page}/"

        html = fetch_page(page_url)
        if not html:
            continue

        page_sounds = extract_animal_sounds_from_html(html)
        print(f"🎵 Найдено звуков на странице: {len(page_sounds)}")
        sounds.extend(page_sounds)

        if len(sounds) >= num_sounds:
            print(f"🎯 Достигнут лимит в {num_sounds} звуков")
            return sounds[:num_sounds]

        time.sleep(1)

    return sounds


def good_filename(name: str) -> str:
    """
    Создает безопасное имя файла из произвольной строки.
    """
    name = re.sub(r'[^a-zA-Z0-9а-яА-ЯёЁ_.-]+', "_", name)
    name = re.sub(r'_+', "_", name)
    name = name.strip("_")
    return name[:100]


def download_sounds(sounds: List[Dict[str, str]],
                    dest_dir: str,
                    csv_path: str) -> None:
    """
    Скачивает звуки и создает CSV файл аннотации.
    """
    os.makedirs(dest_dir, exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[
                                "title", "absolute_path", "relative_path"])
        writer.writeheader()

        for i, sound in enumerate(sounds, start=1):
            safe_name = good_filename(sound["title"])
            filename = f"{i:03d}_{safe_name}.mp3"
            file_path = os.path.join(dest_dir, filename)

            try:
                print(f"⬇️  Скачиваем ({i}/{len(sounds)}): {safe_name}")

                resp = requests.get(
                    sound["mp3_link"], headers=HEADERS, timeout=30)
                resp.raise_for_status()

                if len(resp.content) < 1024:
                    print(f"❌ Файл слишком маленький: {safe_name}")
                    continue

                with open(file_path, "wb") as f:
                    f.write(resp.content)

                abs_path = os.path.abspath(file_path)
                rel_path = os.path.relpath(
                    file_path, start=os.path.dirname(csv_path))

                writer.writerow({
                    "title": sound["title"],
                    "absolute_path": abs_path,
                    "relative_path": rel_path
                })

                print(f"✅ Сохранено: {filename}")

            except Exception as e:
                print(f"❌ Ошибка: {sound['title']}: {e}")


class AudioFileIterator:
    """
    Итератор для работы с путями к аудиофайлам.
    """

    def __init__(self, source: str):
        self.paths = []

        if os.path.isdir(source):
            for root, _, files in os.walk(source):
                for f in files:
                    if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                        self.paths.append(os.path.join(root, f))
        elif os.path.isfile(source) and source.endswith(".csv"):
            with open(source, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "absolute_path" in row:
                        self.paths.append(row["absolute_path"])
        else:
            raise ValueError(
                "Источник должен быть путем к CSV файлу или папке")

        self._index = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self._index >= len(self.paths):
            raise StopIteration
        path = self.paths[self._index]
        self._index += 1
        return path

    def __len__(self) -> int:
        return len(self.paths)


def parse_args():
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Mixkit animal sounds downloader"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Путь к папке для сохранения звуков"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Путь к CSV файлу аннотации"
    )
    parser.add_argument(
        "--min_files",
        type=int,
        default=50,
        help="Минимальное количество файлов"
    )
    parser.add_argument(
        "--max_files",
        type=int,
        default=1000,
        help="Максимальное количество файлов"
    )

    return parser.parse_args()


def main():
    """Основная функция скрипта."""
    args = parse_args()

    print("🎵 Скачиваем звуки животных с Mixkit.co")
    print(f"📁 Папка: {args.folder}")
    print(f"📄 Аннотация: {args.csv}")
    print(f"🎯 Цель: от {args.min_files} до {args.max_files} файлов")

    animal_sounds_url = "https://mixkit.co/free-sound-effects/animals/"

    print("\n🔍 Ищем звуки животных...")
    sounds = fetch_animal_sounds(animal_sounds_url, args.max_files)

    if not sounds:
        print("❌ Не найдено звуков животных")
        return

    print(f"\n🎵 Всего найдено звуков: {len(sounds)}")

    download_sounds(sounds, args.folder, args.csv)

    if len(sounds) < args.min_files:
        print(f"⚠️  ВНИМАНИЕ: Скачано только {len(sounds)} файлов "
              f"из минимально требуемых {args.min_files}")
    else:
        print(f"🎉 Успешно! Скачано {len(sounds)} файлов")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИТЕРАТОРА")
    print("=" * 50)

    print("\n📋 Итератор из файла аннотации:")
    iterator_csv = AudioFileIterator(args.csv)
    print(f"Всего файлов в итераторе: {len(iterator_csv)}")

    print("\nПервые 5 файлов:")
    for i, path in enumerate(iterator_csv):
        if i < 5:
            print(f"  {i+1}. {os.path.basename(path)}")
        else:
            break

    print("\n📁 Итератор из папки:")
    iterator_folder = AudioFileIterator(args.folder)
    print(f"Всего файлов в итераторе: {len(iterator_folder)}")

    print("\nПервые 5 файлов:")
    for i, path in enumerate(iterator_folder):
        if i < 5:
            print(f"  {i+1}. {os.path.basename(path)}")
        else:
            break


if __name__ == "__main__":
    main()