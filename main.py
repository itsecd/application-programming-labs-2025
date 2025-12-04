import argparse
import requests
import os
import csv
import re


from bs4 import BeautifulSoup
from typing import Set


HEADERS = {
    # User-Agent для обхода потенциальных блокировок
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
BASE_URL = "https://mixkit.co"


def get_html(url: str) -> str | None:
    """
    Выполняет HTTP GET запрос и возвращает HTML-содержимое страницы.

    :param url: URL-адрес страницы для загрузки.
    :return: HTML-код страницы в виде строки или None в случае ошибки запроса.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # Вызовет исключение для кодов 4xx/5xx
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        # Ошибка запроса обрабатывается в вызывающей функции
        return None


def extract_sound_page_links(html: str) -> list[str]:
    """
    Извлекает абсолютные URL-адреса страниц отдельных звуков со страницы категории.
    Использует универсальный поиск по шаблону href.

    :param html: HTML-код страницы категории.
    :return: Список полных URL-адресов страниц отдельных звуков.
    """
    soup = BeautifulSoup(html, "html.parser")
    sound_links = []

    for link_tag in soup.find_all("a", href=True):
        href = link_tag.get("href")

        if href and href.startswith("/free-sound-effects/") and len(href) > 25:
            full_url = f"{BASE_URL}{href}"

            if full_url not in sound_links:
                sound_links.append(full_url)

    return sound_links


def extract_file_id(page_html: str) -> str | None:
    """
    Извлекает уникальный ID файла из data-атрибута плеера на странице звука.

    :param page_html: HTML-код страницы отдельного звука.
    :return: Строковый ID файла (например, '2415') или None.
    """
    soup = BeautifulSoup(page_html, "html.parser")

    audio_player_div = soup.find("div", {"data-test-id": "audio-player"})

    if audio_player_div:
        file_id = audio_player_div.get("data-audio-player-item-id-value")
        return file_id
    return None


def get_download_url(file_id: str) -> str:
    """
    Формирует прямую ссылку на скачивание WAV-файла по его ID.

    :param file_id: Уникальный ID файла (например, '2415').
    :return: Прямая ссылка на WAV-файл.
    """
    return f"https://assets.mixkit.co/active_storage/sfx/{file_id}/{file_id}.wav"


def get_annotated_ids(annotation_path: str) -> Set[str]:
    """
    Читает файл аннотации и возвращает набор уже обработанных ID файлов.
    ID извлекаются из имени файла ('sfx_ID.wav') в колонке 'relative_path'.

    :param annotation_path: Путь к файлу аннотации (CSV).
    :return: Набор (Set) уникальных ID, уже записанных в аннотации.
    """
    processed_ids = set()
    if os.path.exists(annotation_path):
        try:
            with open(annotation_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rel_path = row.get("relative_path")
                    if rel_path:
                        # Извлекаем ID из имени файла, например 'sfx_1714.wav' -> '1714'
                        match = re.search(
                            r"sfx_(\d+)\.wav$", os.path.basename(rel_path)
                        )
                        if match:
                            processed_ids.add(match.group(1))
            print(f"Loaded {len(processed_ids)} unique IDs from existing annotation.")
        except IOError:
            print(
                f"Warning: Could not read existing annotation file {annotation_path}. Check file permissions."
            )
        except Exception as e:
            print(
                f"Warning: Error processing annotation file structure: {e}. Starting without ID check."
            )
    return processed_ids


def create_annotation_entry(annotation_path: str, abs_path: str, rel_path: str) -> None:
    """
    Добавляет одну запись (абсолютный и относительный путь) в CSV-файл аннотации.

    :param annotation_path: Путь к файлу аннотации (CSV).
    :param abs_path: Абсолютный путь к сохраненному файлу.
    :param rel_path: Относительный путь к сохраненному файлу.
    :raises Exception: Если произошла ошибка записи в файл.
    """
    fieldnames = ["absolute_path", "relative_path"]
    file_exists = os.path.exists(annotation_path)

    try:
        with open(annotation_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists or os.path.getsize(annotation_path) == 0:
                writer.writeheader()

            writer.writerow({"absolute_path": abs_path, "relative_path": rel_path})
    except IOError as exc:
        # Выбрасываем ошибку, чтобы она была обработана в main
        error_msg = (
            f"Ошибка при записи в файл '{annotation_path}': {exc}. "
            f"Проверьте, не открыт ли файл в другой программе (например, Excel)."
        )
        raise Exception(error_msg)
    except Exception as exc:
        raise Exception(f"Общая ошибка при записи в аннотацию: {exc}")


def download_file(file_id: str, download_url: str, save_path: str) -> str:
    """
    Скачивает файл и сохраняет его на диск.

    :param file_id: Уникальный ID файла (используется для имени).
    :param download_url: Прямая ссылка на файл.
    :param save_path: Локальный путь для сохранения файлов.
    :return: Относительный путь к сохраненному файлу.
    :raises Exception: При ошибке скачивания или записи на диск.
    """
    filename = f"sfx_{file_id}.wav"
    full_filepath = os.path.join(save_path, filename)

    try:
        response = requests.get(download_url, headers=HEADERS, stream=True, timeout=15)
        response.raise_for_status()

        # Запись файла по частям
        with open(full_filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return os.path.relpath(full_filepath)

    except requests.exceptions.RequestException as exc:
        raise Exception(f"Ошибка при скачивании файла {download_url}: {exc}")
    except IOError as exc:
        raise Exception(f"Ошибка при записи файла '{full_filepath}': {exc}")


def process_page_and_annotate(
    page_url: str, save_path: str, annotation_file: str
) -> str | None:
    """
    Обрабатывает одну страницу: получает HTML, извлекает ID, скачивает файл,
    создает запись в аннотации.

    ! Ошибки, возникающие в download_file или create_annotation_entry,
    ! передаются (raise) выше для обработки в main.

    :param page_url: URL страницы отдельного звука.
    :param save_path: Путь к папке для сохранения.
    :param annotation_file: Путь к CSV-файлу аннотации.
    :return: ID успешно скачанного файла или None.
    """
    sound_html = get_html(page_url)
    if not sound_html:
        return None

    file_id = extract_file_id(sound_html)
    if not file_id:
        return None

    download_url = get_download_url(file_id)

    # 1. Скачивание файла
    rel_path = download_file(file_id, download_url, save_path)

    # 2. Аннотирование
    abs_path = os.path.abspath(os.path.join(save_path, f"sfx_{file_id}.wav"))
    create_annotation_entry(annotation_file, abs_path, rel_path)

    print(f"Successfully downloaded and annotated: {rel_path}")
    return file_id


class FilePathIterator:
    """
    Итератор для предоставления абсолютных путей к файлам.
    """

    def __init__(self, source_path: str):
        """
        Конструктор принимает путь к файлу-аннотации или к папке.
        """
        self.paths: list[str] = []
        self.index: int = 0

        if os.path.isdir(source_path):
            for root, _, files in os.walk(source_path):
                for file in files:
                    if not file.startswith("."):
                        self.paths.append(os.path.abspath(os.path.join(root, file)))
        elif os.path.isfile(source_path) and source_path.lower().endswith(".csv"):
            try:
                with open(source_path, "r", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if "absolute_path" in row:
                            self.paths.append(row["absolute_path"])
            except IOError as exc:
                raise ValueError(f"Error reading CSV annotation file: {exc}")
        else:
            # Не бросаем ошибку, если пути не существует, чтобы main мог сначала создать папку.
            # Но бросаем, если путь существует, но не является папкой или CSV.
            if os.path.exists(source_path):
                raise ValueError(
                    "Source path must be a valid directory or CSV annotation file."
                )

    def __iter__(self) -> "FilePathIterator":
        """Возвращает сам объект-итератор, сбрасывая индекс."""
        self.index = 0
        return self

    def __next__(self) -> str:
        """
        Возвращает следующий абсолютный путь к файлу.
        :raises StopIteration: Если все пути были перебраны.
        :return: Абсолютный путь к файлу.
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки, определяя параметры для скачивания.

    :return: Объект Namespace с аргументами.
    """
    parser = argparse.ArgumentParser(
        description="Скрипт для скачивания уникальных аудиофайлов с mixkit.co и создания аннотации."
    )
    parser.add_argument(
        "-c",
        "--category",
        type=str,
        default="nature",
        help="Ключевое слово для поиска на mixkit (например, 'nature').",
    )
    parser.add_argument(
        "-s",
        "--save_path",
        type=str,
        default="nature_sounds",
        help="Путь к папке для сохранения скачанных файлов.",
    )
    parser.add_argument(
        "-a",
        "--annotation_file",
        type=str,
        default="annotation.csv",
        help="Путь к файлу аннотации (CSV).",
    )
    parser.add_argument(
        "-m",
        "--max_num",
        type=int,
        default=50,
        choices=range(50, 1001),
        metavar="[50-1000]",
        help="Максимальное количество файлов для скачивания.",
    )
    return parser.parse_args()


def main() -> None:
    """
    Точка входа: запускает весь процесс скачивания и аннотирования.
    Обработка ошибок критических операций (запросов, диска, аннотации)
    происходит здесь, в главном цикле.
    """
    args = parse_args()

    # Инициализация параметров
    category_slug = f"/free-sound-effects/{args.category.lower().replace(' ', '-')}"
    save_path = args.save_path
    annotation_file = args.annotation_file
    max_downloads = args.max_num

    print(f"--- Starting Download Process ---")
    print(f"Category: {args.category.upper()} | Max Files: {max_downloads}")
    print(f"Save Dir: {save_path} | Annotation File: {annotation_file}")

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    try:
        # 1. Загрузка уже обработанных ID для проверки дубликатов
        processed_ids = get_annotated_ids(annotation_file)

        # 2. Получение списка URL-ов страниц звуков
        category_url = f"{BASE_URL}{category_slug}"
        category_html = get_html(category_url)
        if not category_html:
            print("Aborted: Could not fetch category page.")
            return

        sound_page_urls = extract_sound_page_links(category_html)
        print(f"Found {len(sound_page_urls)} sound pages on the category page.")

        downloaded_count = 0

        # 3. Обход страниц и скачивание
        for page_url in sound_page_urls:
            if len(processed_ids) >= max_downloads:
                print(f"Reached maximum file limit: {max_downloads}")
                break

            # Получение HTML и ID для проверки дубликатов
            sound_html = get_html(page_url)
            if not sound_html:
                continue

            file_id = extract_file_id(sound_html)

            if not file_id:
                continue

            if file_id in processed_ids:
                # Проверка на дубликат
                continue

            try:
                # В process_page_and_annotate содержится вся логика: скачивание + аннотирование.
                # Ошибки из него (IO, requests) пробрасываются сюда.
                success_id = process_page_and_annotate(
                    page_url, save_path, annotation_file
                )

                if success_id:
                    processed_ids.add(success_id)
                    downloaded_count += 1

            except Exception as e:
                # Ошибка при обработке текущей страницы (скачивание/запись),
                # выводим сообщение и переходим к следующей странице.
                print(f"Error processing page {page_url} (ID: {file_id}): {e}")
                continue

        print(f"\n--- Process Complete ---")
        print(f"New files downloaded: {downloaded_count}")
        print(f"Total unique files processed: {len(processed_ids)}")

        # 4. Демонстрация работы итератора
        print("\n--- Testing FilePathIterator ---")
        try:
            annot_iterator = FilePathIterator(annotation_file)
            print(f"Paths found in annotation file: {len(annot_iterator.paths)}")
            for elem in annot_iterator:
                print(elem)
        except ValueError as e:
            print(f"Error initializing iterator from annotation file: {e}")

        try:
            dir_iterator = FilePathIterator(save_path)
            print(f"Files found in directory: {len(dir_iterator.paths)}")
            for elem in annot_iterator:
                print(elem)
        except ValueError as e:
            print(f"Error initializing iterator from save path: {e}")

    except Exception as e:
        # Обработка фатальной ошибки, которая остановила весь процесс (например,
        # ошибка парсинга аргументов, невозможность создать папку и т.д.)
        print(f"\nFatal Error: {e}")


if __name__ == "__main__":
    main()
