import csv
from pathlib import Path
from icrawler.builtin import BingImageCrawler
import argparse


def cra(query: list[str], images_dir: Path, count: int) -> None:
    """Скачивает изображения с Bing по заданным ключевым словам.

    Для каждого ключевого слова создаёт поддиректорию в images_dir
    и скачивает указанное количество изображений.

    Args:
        query (List[str]): Список поисковых запросов (ключевых слов).
        images_dir (Path): Базовая директория для сохранения изображений.
        count (int): Максимальное количество изображений на запрос.

    Side Effects:
        Создаёт поддиректории и сохраняет изображения на диск.
    """
    for keyword in query:
        folder = images_dir / keyword
        crawler = BingImageCrawler(
            storage={"root_dir": str(folder)},
            parser_threads=2,
            downloader_threads=4
        )
        print(f"Скачивание по запросу: {keyword}")
        crawler.crawl(keyword=keyword, max_num=count)


def annotation_downloaded_files(images_dir: Path, annotation: Path) -> None:
    """Создаёт CSV-аннотацию для изображений .

    Формат строки: filename;absolute_path;relative_path.
    Относительный путь вычисляется от текущей рабочей директории (cwd).
    Поддерживает только прямые поддиректории в images_dir (не рекурсивно).

    Args:
        images_dir (Path): Директория с подпапками, содержащими изображения.
        annotation (Path): Путь к выходному CSV-файлу.

    Side Effects:
        Создаёт родительские директории для annotation и записывает файл.
        Если images_dir не существует — создаёт пустой CSV.
    """
    annotation.parent.mkdir(parents=True, exist_ok=True)

    if not images_dir.exists():
        with open(annotation, 'w', encoding='utf-8-sig') as f:
            pass  # пустой файл
        return

    rows = []
    for subdir in images_dir.iterdir():
        if subdir.is_dir():
            for img in subdir.iterdir():
                if img.is_file():
                    abs_path = img.resolve()
                    rel_path = abs_path.relative_to(Path.cwd())
                    rows.append([img.name, str(abs_path), str(rel_path)])

    with open(annotation, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Скачивание изображений и создание аннотации")
    parser.add_argument('--images_dir', type=Path, required=True ,help='images_dir например "images" ')
    parser.add_argument('--annotation', type=Path, default=Path("annotation.csv"), help='annotation например "annotation.csv"')
    parser.add_argument('--query', nargs='+', type=str , help='keyword например "машина природа"')
    parser.add_argument('--count', type=int, default=2,help='количество фото')

    args = parser.parse_args()


    if args.query:
        cra(args.query, args.images_dir, args.count)
        annotation_downloaded_files(args.images_dir, args.annotation)

    if args.annotation.exists():
        source = args.annotation 
    else:
        source = args.images_dir
        
    try:
        it = ImageFileIterator(source)
        print('\n')
        for path in it:
            print(path)
        print("")
        for path in it:
            print(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка итератора: {e}")


if __name__ == "__main__":
    main()