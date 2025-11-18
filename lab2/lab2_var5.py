import argparse
import csv
from pathlib import Path

from icrawler.builtin import GoogleImageCrawler


def parse_args() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки: цвет, количество, папка, путь к CSV и ключевое слово.
    """
    parser = argparse.ArgumentParser(description="ЛР: скачивание изображений по цвету и создание CSV-аннотации")
    parser.add_argument("--color", required=True, choices=["red", "yellow", "green", "blue"], help="Цвет изображений (red, yellow, green, blue)")
    parser.add_argument("--count", type=int, required=True, help="Количество изображений для скачивания (от 50 до 1000)")
    parser.add_argument("--save-dir", required=True, help="Папка для сохранения изображений")
    parser.add_argument("--csv", required=True, help="Путь к CSV-файлу аннотации")
    parser.add_argument("--keyword", default="bird", help='Ключевое слово поиска (по умолчанию "bird")')
    return parser.parse_args()

def download_images(keyword: str, color: str, save_dir: Path, count: int) -> None:
    """
    Скачивает изображения через BingImageCrawler по запросу, включающему цвет и ключевое слово.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": str(save_dir)}, feeder_threads=1, parser_threads=1, downloader_threads=4)
    filters = {"color" : color, "size": "large", "type" : "photo"}
    crawler.crawl(keyword=keyword, max_num=count, filters=filters, file_idx_offset=0)

def write_csv_annotation(folder: Path, csv_path: Path) -> None:
    """
    Создаёт CSV-файл с абсолютными и относительными путями всех изображений из указанной папки.
    """
    base = folder.resolve()
    files = [p.resolve() for p in base.rglob("*") if p.is_file()]
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path"])
        for abs_path in files:
            rel_path = abs_path.relative_to(base)
            writer.writerow([str(abs_path), str(rel_path)])


class PathIterator:
    """
    Итератор, который возвращает пути к файлам из CSV-аннотации или папки.
    """
    def __init__(self, csv_path: Path | None = None, folder_path: Path | None = None) -> None:
        """
        Сохраняет путь к CSV или папке, проверяет, что указан хотя бы один источник.
        """
        if csv_path is None and folder_path is None:
            raise ValueError("Нужно указать путь к CSV/путь к папке.")
        self.csv_path = csv_path
        self.folder_path = folder_path

    def __iter__(self):
        """
        Возвращает генератор путей (Path) из CSV-файла или из папки.
        """
        if self.csv_path is not None:
            with self.csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    abs_str = (row.get("absolute_path") or "").strip()
                    if abs_str:
                        yield Path(abs_str)
        else:
            base = Path(self.folder_path).resolve()
            for p in base.rglob("*"):
                if p.is_file():
                    yield p


def main() -> None:
    """
    Главная функция.
    """
    args = parse_args()

    if not (50 <= args.count <= 1000):
        raise ValueError("Ошибка: --count должен быть в диапазоне от 50 до 1000 изображений. ")
        return

    print(f"Скачивание {args.count} изображений по запросу: '{args.color} {args.keyword}'")
    download_images(
        keyword=args.keyword,
        color=args.color,
        save_dir=Path(args.save_dir),
        count=args.count
    )

    print(f"Создание CSV-аннотации: {args.csv}")
    write_csv_annotation(
        folder=Path(args.save_dir),
        csv_path=Path(args.csv)
    )

    print("Первые несколько путей из CSV через итератор:")
    for i, path in zip(range(5), PathIterator(csv_path=Path(args.csv))):
        print("-", path)


if __name__ == "__main__":
    main()