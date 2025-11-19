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