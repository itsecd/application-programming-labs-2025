import argparse
import csv
import requests
import os
import time
import random
import re

from bs4 import BeautifulSoup


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Скачивание звуков с mixkit.co (только >10 секунд)"
    )

    parser.add_argument(
        "--download-folder",
        "-d",
        required=True,
        help="Папка для сохранения аудиофайлов",
    )
    parser.add_argument(
        "--min-files", type=int, default=50, help="Минимальное количество файлов"
    )
    parser.add_argument(
        "--max-files", type=int, default=100, help="Максимальное количество файлов"
    )

    args = parser.parse_args()

    # Валидация аргументов
    if not (50 <= args.max_files <= 1000):
        parser.error("--max-files должно быть от 50 до 1000")
    if args.min_files > args.max_files:
        parser.error("--min-files не может быть больше --max-files")

    return args


class SoundDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        )
        self.base_url = "https://mixkit.co"

    def get_sound_pages(self):
        """Получить страницы со звуками из разных разделов"""
        sound_pages = []

        sections = [
            "/free-sound-effects/",
            "/free-sound-effects/animals/",
            "/free-sound-effects/cartoon/",
            "/free-sound-effects/city/",
            "/free-sound-effects/nature/",
            "/free-sound-effects/people/",
            "/free-sound-effects/science-fiction/",
            "/free-sound-effects/sports/",
            "/free-sound-effects/technology/",
            "/free-sound-effects/transportation/",
        ]

        for section in sections:
            if len(sound_pages) >= 100:
                break

            url = self.base_url + section
            print(f"Поиск в разделе: {section}")

            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, "html.parser")

                # Ищем ссылки на отдельные звуки
                all_links = soup.find_all("a", href=True)

                for link in all_links:
                    href = link["href"]
                    # Ищем ссылки вида /free-sound-effects/название-звука-123/
                    if href.startswith("/free-sound-effects/") and href.count("/") == 3:
                        full_url = self.base_url + href
                        if full_url not in sound_pages:
                            sound_pages.append(full_url)

                time.sleep(1)

            except Exception as e:
                raise Exception(f"Ошибка при парсинге раздела {section}: {e}")

        return sound_pages

    def parse_duration(self, duration_str):
        """Преобразует строку длительности в секунды"""
        if not duration_str:
            return 0

        duration_str = duration_str.strip()

        # Убираем лишние пробелы и символы
        duration_str = re.sub(r"\s+", "", duration_str)

        # Формат "0:01" или "1:23"
        if ":" in duration_str:
            parts = duration_str.split(":")
            if len(parts) == 2:
                try:
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    return minutes * 60 + seconds
                except ValueError:
                    return 0

        # Пытаемся найти числа в строке
        numbers = re.findall(r"\d+", duration_str)
        if numbers:
            # Если только одно число, считаем это секундами
            if len(numbers) == 1:
                return int(numbers[0])
            # Если два числа, считаем это минутами:секундами
            elif len(numbers) == 2:
                return int(numbers[0]) * 60 + int(numbers[1])

        return 0

    def get_duration_and_audio_url(self, page_url):
        """Извлекает длительность и аудио URL со страницы звука"""
        try:
            response = self.session.get(page_url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Ищем длительность по классу
            duration_elem = soup.find("div", class_="item-grid-sfx-preview__meta-time")
            if not duration_elem:
                # Альтернативный поиск по data-test-id
                duration_elem = soup.find("div", {"data-test-id": "duration"})

            duration_sec = 0
            if duration_elem:
                duration_text = duration_elem.get_text(strip=True)
                duration_sec = self.parse_duration(duration_text)
                print(f"Найдена длительность: {duration_text} -> {duration_sec} сек")

            # Аудио URL из data-атрибута
            audio_div = soup.find("div", {"data-audio-player-preview-url-value": True})
            audio_url = None
            if audio_div:
                audio_url = audio_div.get("data-audio-player-preview-url-value")

            return duration_sec, audio_url

        except Exception as e:
            print(f"Ошибка извлечения данных со страницы {page_url}: {e}")
            return 0, None

    def download_sound_from_page(self, page_url, download_folder, min_duration=10):
        """Скачивает звук, только если его длительность > min_duration"""
        duration_sec, audio_url = self.get_duration_and_audio_url(page_url)

        if duration_sec <= min_duration:
            print(f"Пропущен (слишком короткий: {duration_sec} сек): {page_url}")
            return None, None

        if not audio_url:
            print(f"Не найден аудио URL: {page_url}")
            return None, None

        if not audio_url.startswith("http"):
            print(f"Некорректный аудио URL: {audio_url}")
            return None, None

        # Формируем имя файла
        filename = os.path.basename(audio_url)
        if not filename.endswith(".mp3"):
            filename += ".mp3"
        filepath = os.path.join(download_folder, filename)

        # Скачиваем файл
        print(f"Скачивание ({duration_sec} сек): {filename}")
        try:
            audio_response = self.session.get(audio_url, timeout=30)
            if audio_response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(audio_response.content)

                # Проверяем что файл скачался
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    return filepath, filename
                else:
                    print(f"Файл не скачался или пустой: {filename}")
                    return None, None
            else:
                print(
                    f"Ошибка HTTP {audio_response.status_code} при скачивании: {audio_url}"
                )
        except Exception as e:
            print(f"Ошибка скачивания {filename}: {e}")

        return None, None

    def download_sounds(
        self, download_folder, min_files=50, max_files=1000, min_duration=10
    ):
        """Основной метод скачивания звуков"""
        os.makedirs(download_folder, exist_ok=True)
        annotation_file = os.path.join(download_folder, "annotation.csv")

        print("Поиск страниц со звуками...")
        sound_pages = self.get_sound_pages()
        print(f"Найдено потенциальных звуков: {len(sound_pages)}")

        with open(annotation_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["absolute_path", "relative_path", "filename", "duration_seconds"]
            )

            downloaded = 0
            for i, page_url in enumerate(sound_pages):
                if downloaded >= max_files:
                    break

                print(f"\n--- Обработка {i + 1}/{len(sound_pages)} ---")
                filepath, filename = self.download_sound_from_page(
                    page_url, download_folder, min_duration
                )

                if filepath and os.path.exists(filepath):
                    absolute_path = os.path.abspath(filepath)
                    relative_path = os.path.relpath(filepath, download_folder)

                    # Получаем длительность для записи в CSV
                    duration_sec, _ = self.get_duration_and_audio_url(page_url)

                    writer.writerow(
                        [absolute_path, relative_path, filename, duration_sec]
                    )
                    downloaded += 1
                    print(
                        f"Сохранён: {filename} ({duration_sec} сек) [{downloaded}/{max_files}]"
                    )
                else:
                    print("Пропущен или ошибка загрузки")

                # Задержка между запросами
                time.sleep(random.uniform(1, 2))

        print(f"\n Завершено! Скачано файлов: {downloaded}")
        if downloaded < min_files:
            print(f" Внимание: скачано меньше минимального количества ({min_files})")

        return annotation_file


class SoundIterator:
    def __init__(self, annotation_source):
        """Итератор по аудиофайлам. Принимает путь к CSV или папке."""
        self.file_paths = []

        if os.path.isfile(annotation_source):
            # Загрузка из CSV
            with open(annotation_source, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # пропуск заголовка
                for row in reader:
                    if row and len(row) > 0:
                        abs_path = row[0]
                        if os.path.exists(abs_path):
                            self.file_paths.append(abs_path)
            print(f"Загружено {len(self.file_paths)} путей из аннотации")
        elif os.path.isdir(annotation_source):
            # Загрузка из папки
            for root, _, files in os.walk(annotation_source):
                for file in files:
                    if file.lower().endswith((".mp3", ".wav", ".ogg")):
                        self.file_paths.append(os.path.join(root, file))
            print(f"Загружено {len(self.file_paths)} файлов из папки")
        else:
            raise ValueError(
                f"Укажите существующий CSV-файл или папку: {annotation_source}"
            )

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.file_paths):
            path = self.file_paths[self._index]
            self._index += 1
            return path
        else:
            raise StopIteration

    def __len__(self):
        return len(self.file_paths)


def main():
    """Основная функция программы"""
    # Парсим аргументы командной строки
    args = parse_arguments()

    # Скачивание звуков
    downloader = SoundDownloader()
    annotation_path = downloader.download_sounds(
        download_folder=args.download_folder,
        min_files=args.min_files,
        max_files=args.max_files,
        min_duration=10,
    )

    # Демонстрация итератора
    if annotation_path and os.path.exists(annotation_path):
        print("\n" + "=" * 50)
        print("Демонстрация работы итератора:")
        print("=" * 50)

        iterator = SoundIterator(annotation_path)
        print(f"Всего файлов для итерации: {len(iterator)}")

        print("\nПервые 5 файлов:")
        for i, path in enumerate(iterator):
            if i < 5:
                print(f"{i + 1}: {os.path.basename(path)}")

        print("...")


if __name__ == "__main__":
    main()
