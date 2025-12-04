import argparse
import csv
import os
import threading
import time
from typing import Iterator
from icrawler.builtin import BingImageCrawler


class FilePathIterator:
    """Итератор для обхода файлов в директории и записи в CSV с диапазонами размеров"""

    def __init__(
        self,
        dirpath: str,
        csvfile: str,
        script_dir: str,
        size_ranges: list[tuple[list[int], list[int]]] = None,
    ):
        if not os.path.exists(dirpath):
            raise ValueError(f"Директория '{dirpath}' не найдена")

        self.dirpath = dirpath
        self.csvfile = csvfile if csvfile.endswith(".csv") else csvfile + ".csv"
        self.script_dir = script_dir
        self.size_ranges = size_ranges or []

        self.file_paths = self._collect_files()
        self.index = 0

    def _collect_files(self) -> list[str]:
        """Собирает все файлы из директории рекурсивно (исключая CSV)"""
        files = []
        for root, dirs, filenames in os.walk(self.dirpath):
            for filename in sorted(filenames):
                # Пропускаем CSV файлы.
                if filename.endswith(".csv"):
                    continue
                files.append(os.path.join(root, filename))
        return files

    def _get_image_size(self, filepath: str) -> tuple[int, int]:
        """Получаю размеры изображения через OpenCV"""
        try:
            import cv2

            img = cv2.imread(filepath)
            if img is None:
                return 0, 0
            height, width = img.shape[:2]
            return height, width
        except Exception as e:
            print(f"Ошибка получения размера {filepath}: {e}")
            return 0, 0

    def _find_size_range(self, height: int, width: int) -> int:
        """Определяет номер диапазона размеров для файла"""
        for i, (max_size, min_size) in enumerate(self.size_ranges, 1):
            max_h, max_w = max_size
            min_h, min_w = min_size

            if min_h <= height <= max_h and min_w <= width <= max_w:
                return i

        return 0

    def _get_existing_paths(self) -> set:
        """Получает все уже записанные пути из CSV"""
        existing_paths = set()

        if not os.path.exists(self.csvfile):
            return existing_paths

        try:
            with open(self.csvfile, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Пропускаем заголовок
                for row in reader:
                    if row:
                        existing_paths.add(row[0])  # Абсолютный путь
        except Exception as e:
            print(f"Ошибка при чтении CSV: {e}")

        return existing_paths

    """Реализация итератора"""

    def __iter__(self) -> Iterator[str]:
        """Возвращает сам итератор"""
        self.index = 0
        return self

    def __next__(self) -> str:
        """Возвращает следующий файл"""
        if self.index >= len(self.file_paths):
            raise StopIteration

        file_path = self.file_paths[self.index]
        self.index += 1
        return file_path

    def __len__(self) -> int:
        """Возвращает количество файлов"""
        return len(self.file_paths)

    def init_csv(self) -> None:
        """Инициализирует CSV с заголовком"""
        headers = ["Абсолютный путь", "Относительный путь", "Высота", "Ширина"]
        with open(self.csvfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def write_all(self) -> None:
        """Записывает все файлы из итератора в CSV без дубликатов с определением диапазона"""
        existing_paths = self._get_existing_paths()
        added_count = 0
        skipped_count = 0
        range_stats: dict[int, int] = {}

        for file_path in self:
            abs_path = os.path.abspath(file_path)

            # Пропускаем если уже есть в CSV.
            if abs_path in existing_paths:
                skipped_count += 1
                continue

            # Получаем размеры изображения.
            height, width = self._get_image_size(abs_path)
            range_num = self._find_size_range(height, width)
            rel_path = os.path.relpath(abs_path, self.script_dir)

            with open(self.csvfile, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([abs_path, rel_path, height, width])

            existing_paths.add(abs_path)
            added_count += 1

        print(f"Добавлено: {added_count} файлов")
        if skipped_count > 0:
            print(f"Пропущено дубликатов: {skipped_count}")

        if range_stats:
            print("\nСтатистика по диапазонам:")
            for range_num in sorted(range_stats.keys()):
                count = range_stats[range_num]
                if range_num > 0:
                    max_h, max_w = self.size_ranges[range_num - 1][0]
                    min_h, min_w = self.size_ranges[range_num - 1][1]
                    print(
                        f"Диапазон {range_num} ({min_h}x{min_w} - {max_h}x{max_w}): {count} файлов"
                    )
                else:
                    print(f"Вне диапазонов: {count} файлов")


def parse_size_pair(s: str) -> list[int]:
    """Парсит строку формата '1920x1080' в [высота, ширина]"""
    try:
        if "x" in s.lower():
            height, width = s.lower().split("x")
        else:
            height, width = s.split(",")
        return [int(height), int(width)]
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Неверный формат: '{s}'. Используйте 'высотаxширина' (например: 1920x1080)"
        )


def validate_size_ranges(size_ranges: list[tuple[list[int], list[int]]]) -> None:
    """Проверка диапазонов размеров на корректность"""
    for i, (max_size, min_size) in enumerate(size_ranges, 1):
        max_h, max_w = max_size
        min_h, min_w = min_size

        if max_h <= 0 or max_w <= 0 or min_h <= 0 or min_w <= 0:
            raise ValueError(f"Диапазон {i}: все размеры должны быть > 0")

        if max_h <= min_h or max_w <= min_w:
            raise ValueError(
                f"Диапазон {i}: максимальные размеры должны быть больше минимальных"
            )


def add_to_csv(csvfile: str, filepath: str, script_dir: str) -> None:
    """Добавляет один файл в CSV"""
    abs_path = os.path.abspath(filepath)
    rel_path = os.path.relpath(abs_path, script_dir)

    with open(csvfile, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([abs_path, rel_path])


def create_directory(dirname: str) -> None:
    """Создаёт директорию если её нет"""
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f"Создана директория '{dirname}'")


def monitor_directory(
    dirname: str,
    csvfile: str,
    script_dir: str,
    duration: int,
    size_ranges: list[tuple[list[int], list[int]]] = None,
) -> None:
    """Мониторит директорию и добавляет новые файлы в CSV в реальном времени"""
    import cv2

    tracked_files = set()  # Пути обработанных файлов.
    start_time = time.time()
    size_ranges = size_ranges or []

    while time.time() - start_time < duration:
        try:
            for root, dirs, files in os.walk(dirname):
                for file in files:
                    if file.endswith(".csv"):  # Пропускаем CSV
                        continue

                    # Обработка найденных файлов.
                    file_path = os.path.join(root, file)
                    if file_path not in tracked_files:
                        tracked_files.add(file_path)

                        # Получаем размеры.
                        img = cv2.imread(file_path)
                        if img is not None:
                            height, width = img.shape[:2]
                        else:
                            height, width = 0, 0

                        # Записываем с размерами.
                        abs_path = os.path.abspath(file_path)
                        rel_path = os.path.relpath(abs_path, script_dir)

                        with open(csvfile, "a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow([abs_path, rel_path, height, width])

                        print(f"✅ {file}")
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")

        time.sleep(0.5)  # Пауза, чтобы обновлять список.


def crawl_images(
    dirname: str, num_images: int, max_size: list[int], min_size: list[int]
) -> None:
    """Загружает изображения кроликов с заданными параметрами"""
    bing_crawler = BingImageCrawler(
        storage={"root_dir": dirname},
        downloader_threads=5,  # количество потоков, которые одновременно скачивают изображения.
        feeder_threads=5,  # кол-во потоков (получение и подача URL страниц для поиска изображений).
        parser_threads=5,  # количество потоков, которые парсят загруженные HTML страницы, извлекая оттуда ссылки на сами изображения.
    )
    bing_crawler.downloader.retry_num = 5  # кол-во попыток.
    bing_crawler.crawl(
        keyword="rabbit", max_num=num_images, max_size=max_size, min_size=min_size
    )


def download_images(
    dirname: str,
    num_per_range: int,
    max_size: list[int],
    min_size: list[int],
    csvfile: str,
    script_dir: str,
    range_num: int,
    total_ranges: int,
) -> None:
    """Координирует загрузку изображений с мониторингом в отдельную папку и CSV"""
    # Создаём отдельную директорию для каждого диапазона.
    range_dir = os.path.join(dirname, f"range_{range_num}")
    create_directory(range_dir)

    # Создаём отдельный CSV для каждого диапазона.
    range_csv = os.path.join(range_dir, f"range_{range_num}.csv")

    print(
        f"\n[{range_num}/{total_ranges}] Диапазон: {min_size[0]}x{min_size[1]} - {max_size[0]}x{max_size[1]}"
    )
    print(f"Директория: {range_dir}")
    print(f"CSV файл: {range_csv}")
    print(f"Загрузка {num_per_range} изображений..")

    # Инициализируем CSV для этого диапазона.
    iterator = FilePathIterator(range_dir, range_csv, script_dir, [])
    iterator.init_csv()

    # Запускаем мониторинг в отдельном потоке.
    monitor_thread = threading.Thread(
        target=monitor_directory,
        args=(range_dir, range_csv, script_dir, 500),
        daemon=True,
    )
    monitor_thread.start()

    # Загружаем изображения в отдельную папку.
    crawl_images(range_dir, num_per_range, max_size, min_size)

    # Ждём завершения мониторинга.
    time.sleep(2)
    monitor_thread.join(timeout=5)
    print("Диапазон завершён.")


def _parse_cli_args():
    """Парсит CLI аргументы"""
    parser = argparse.ArgumentParser(
        description="Загрузка изображений кроликов с разными размерами"
    )
    parser.add_argument(
        "--directory",
        "-d",
        default="image",
        type=str,
        help="Путь к директории для сохранения (default: image)",
    )
    parser.add_argument(
        "--csvfile",
        "-c",
        default="data.csv",
        type=str,
        help="CSV файл для результатов (default: data.csv)",
    )
    parser.add_argument(
        "--count",
        "-n",
        default=500,
        type=int,
        help="Общее количество изображений (default: 500)",
    )
    parser.add_argument(
        "--max-size",
        action="append",
        type=parse_size_pair,
        dest="max_sizes",
        help="Максимальный размер (например: 1920x1080)",
    )
    parser.add_argument(
        "--min-size",
        action="append",
        type=parse_size_pair,
        dest="min_sizes",
        help="Минимальный размер (например: 640x480)",
    )
    return parser.parse_args()


def _resolve_size_ranges(max_sizes, min_sizes) -> list[tuple[list[int], list[int]]]:
    """Определяет диапазоны размеров из аргументов или берёт по умолчанию"""
    if max_sizes and min_sizes:
        if len(max_sizes) != len(min_sizes):
            raise ValueError(
                f"Количество --max-size ({len(max_sizes)}) != --min-size ({len(min_sizes)})"
            )

        size_ranges = list(zip(max_sizes, min_sizes))
        validate_size_ranges(size_ranges)
        return size_ranges

    # Значения по умолчанию
    return [
        ([1920, 1080], [640, 480]),
        ([1024, 768], [512, 384]),
        ([800, 600], [400, 300]),
    ]


def parse_arguments() -> tuple[str, str, int, list[tuple[list[int], list[int]]]]:
    """Парсит аргументы командной строки"""
    args = _parse_cli_args()
    size_ranges = _resolve_size_ranges(args.max_sizes, args.min_sizes)

    return args.directory, args.csvfile, args.count, size_ranges


def calculate_images_per_range(total_count: int, num_ranges: int) -> tuple[int, int]:
    """Вычисляет количество изображений на диапазон и остаток"""
    num_per_range = total_count // num_ranges
    remainder = total_count % num_ranges
    return num_per_range, remainder


def process_size_ranges(
    directory: str,
    csvfile: str,
    size_ranges: list[tuple[list[int], list[int]]],
    num_per_range: int,
    remainder: int,
    script_dir: str,
) -> None:
    """Обрабатывает все диапазоны размеров"""

    for i, (max_size, min_size) in enumerate(size_ranges, 1):
        # Последний диапазон получает остаток.
        count = num_per_range + (remainder if i == len(size_ranges) else 0)
        download_images(
            directory,
            count,
            max_size,
            min_size,
            csvfile,
            script_dir,
            i,
            len(size_ranges),
        )


def main():
    # Парсим аргументы.
    directory, csvfile, total_count, size_ranges = parse_arguments()

    # Создаём корневую директорию.
    create_directory(directory)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Вычисляем кол-во на диапазон.
    num_per_range, remainder = calculate_images_per_range(total_count, len(size_ranges))

    print(f"\nЗагрузка {total_count} изображений в {len(size_ranges)} диапазонах")

    # Обрабатываем диапазоны.
    process_size_ranges(
        directory, csvfile, size_ranges, num_per_range, remainder, script_dir
    )

    # Создаём общий CSV со всеми файлами.
    print(f"\nСоздание общего CSV файла '{csvfile}'...")
    master_iterator = FilePathIterator(directory, csvfile, script_dir, size_ranges)
    master_iterator.init_csv()
    master_iterator.write_all()

    print("\nЗавершено!")


if __name__ == "__main__":
    main()
