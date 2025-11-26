import argparse
import os
import csv
import random
from pathlib import Path
from icrawler.builtin import BingImageCrawler
import sys


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Web Scraping - Скачивание изображений"
    )

    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Ключевые слова для поиска (через запятую)",
    )

    parser.add_argument(
        "--count",
        type=int,
        required=True,
        choices=range(50, 1001),
        help="Общее количество изображений (50-1000)",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Путь к папке для сохранения изображений",
    )

    parser.add_argument(
        "--annotation_file",
        type=str,
        required=True,
        help="Путь к файлу аннотации (CSV)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Таймаут для скачивания в секундах (по умолчанию 15)",
    )

    return parser.parse_args()


def download_images_for_keyword(
    keyword: str, count: int, output_dir: str, timeout: int = 15
) -> list:
    """
    Скачивает изображения для одного ключевого слова за одну попытку.
    """
    keyword_clean = keyword.strip().replace(" ", "_")
    keyword_dir = os.path.join(output_dir, keyword_clean)

    os.makedirs(keyword_dir, exist_ok=True)

    print(f"Скачивание изображений для: '{keyword}'")

    try:
        crawler = BingImageCrawler(
            storage={"root_dir": keyword_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=2,
        )

        # Настраиваем таймаут
        crawler.downloader.timeout = timeout

        # Скачиваем изображения
        crawler.crawl(keyword=keyword, max_num=count, file_idx_offset="auto")

        # Получаем список скачанных файлов
        downloaded_files = []
        for file_path in Path(keyword_dir).rglob("*.*"):
            if (
                file_path.is_file()
                and file_path.stat().st_size > 0
                and file_path.suffix.lower()
                in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
            ):
                downloaded_files.append(str(file_path))

        print(f"Успешно скачано {len(downloaded_files)} изображений для '{keyword}'")
        return downloaded_files

    except Exception as e:
        print(f"Ошибка при скачивании для '{keyword}': {e}")
        return []


def download_images(
    keywords: list, total_count: int, output_dir: str, timeout: int = 15
) -> list:
    """
    Основная функция скачивания изображений (одна попытка).
    """
    # Рассчитываем сколько изображений нужно для каждого ключевого слова
    images_per_keyword = max(1, total_count // len(keywords))

    print(f"Цель: {total_count} изображений всего")
    print(f"По {images_per_keyword} изображений на каждое ключевое слово")
    print("-" * 50)

    all_downloaded_files = []

    # Скачиваем изображения для каждого ключевого слова (одна попытка)
    for keyword in keywords:
        files = download_images_for_keyword(
            keyword, images_per_keyword, output_dir, timeout
        )
        all_downloaded_files.extend(files)

    # Обрезаем до точного общего количества
    final_files = all_downloaded_files[:total_count]

    return final_files


def create_annotation(
    downloaded_files: list, output_dir: str, annotation_file: str
) -> None:
    """
    Создает CSV-аннотацию с путями к файлам.
    """
    with open(annotation_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["absolute_path", "relative_path", "keyword"])

        for file_path in downloaded_files:
            absolute_path = os.path.abspath(file_path)
            relative_path = os.path.relpath(file_path, output_dir)
            keyword = os.path.basename(os.path.dirname(file_path))
            writer.writerow([absolute_path, relative_path, keyword])

    print(f"Аннотация создана: {annotation_file}")
    print(f"Записано {len(downloaded_files)} записей")


class ImagePathIterator:
    """
    Итератор по путям к файлам изображений.
    """

    def __init__(self, source: str):
        self.source = source
        self.file_paths = []
        self.current_index = 0

        if os.path.isfile(source) and source.endswith(".csv"):
            self._load_from_annotation(source)
        elif os.path.isdir(source):
            self._load_from_directory(source)
        else:
            raise ValueError("Источник должен быть CSV-файлом или папкой")

    def _load_from_annotation(self, annotation_file: str):
        try:
            with open(annotation_file, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if os.path.exists(row["absolute_path"]):
                        self.file_paths.append(row["absolute_path"])
        except Exception as e:
            print(f"Ошибка при чтении аннотации: {e}")

    def _load_from_directory(self, directory: str):
        for root, _, files in os.walk(directory):
            for file in files:
                if self._is_image_file(file):
                    self.file_paths.append(os.path.join(root, file))

    def _is_image_file(self, filename: str) -> bool:
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        return any(filename.lower().endswith(ext) for ext in image_extensions)

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self) -> str:
        if self.current_index < len(self.file_paths):
            path = self.file_paths[self.current_index]
            self.current_index += 1
            return path
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self.file_paths)

    def get_keyword_stats(self) -> dict:
        stats = {}
        for path in self.file_paths:
            keyword = os.path.basename(os.path.dirname(path))
            stats[keyword] = stats.get(keyword, 0) + 1
        return stats


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        args = parse_arguments()
        keywords = [kw.strip() for kw in args.keywords.split(",")]
        output_dir = os.path.abspath(args.output_dir)
        annotation_file = os.path.abspath(args.annotation_file)

        os.makedirs(output_dir, exist_ok=True)

        print("Начало скачивания изображений...")
        print(f"Ключевые слова: {keywords}")
        print(f"Общее количество изображений: {args.count}")
        print(f"Выходная папка: {output_dir}")
        print(f"Файл аннотации: {annotation_file}")
        print(f"Таймаут скачивания: {args.timeout} секунд")
        print("-" * 50)

        downloaded_files = download_images(
            keywords, args.count, output_dir, args.timeout
        )

        if not downloaded_files:
            print("Не удалось скачать ни одного изображения")
            return

        create_annotation(downloaded_files, output_dir, annotation_file)

        print("\nДемонстрация работы итератора:")
        iterator = ImagePathIterator(annotation_file)
        print(f"Всего файлов для итерации: {len(iterator)}")

        stats = iterator.get_keyword_stats()
        print("\nСтатистика по ключевым словам:")
        for keyword, count in stats.items():
            print(f"  {keyword}: {count} изображений")

        print("\nПервые 5 файлов:")
        for i, file_path in enumerate(iterator):
            if i >= 5:
                break
            file_size = os.path.getsize(file_path) / 1024
            print(f"  {i + 1}. {file_path} ({file_size:.1f} KB)")

        print(f"\nПрограмма завершена успешно!")
        print(f"Скачано реальных изображений: {len(downloaded_files)}")

    except Exception as e:
        print(f"Ошибка выполнения программы: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
