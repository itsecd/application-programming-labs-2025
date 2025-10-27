import argparse
import os
from typing import Any
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    :return: Объект argparse.Namespace с параметрами.
    """
    parser = argparse.ArgumentParser(
        description="Скачивание изображений 'hedgehog' "
                    "с помощью icrawler из выбранного источника."
    )

    parser.add_argument(
        "--crawler",
        type=str,
        required=True,
        choices=["google", "bing", "flickr"],
        help="Источник для скачивания изображений: google | bing | flickr"
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Путь к папке для сохранения изображений"
    )

    parser.add_argument(
        "--num",
        type=int,
        default=100,
        help="Количество изображений (от 50 до 1000)"
    )

    return parser.parse_args()


def ensure_directory(path: str) -> None:
    """
    Проверяет существование директории и создаёт её при необходимости.

    :param path: Путь к директории.
    """
    os.makedirs(path, exist_ok=True)


def validate_num_images(num: int) -> None:
    """
    Проверяет корректность количества изображений.

    :param num: Количество изображений.
    :raises ValueError: если число вне диапазона [50, 1000].
    """
    if not (50 <= num <= 1000):
        raise ValueError("Количество изображений должно быть от 50 до 1000.")


def create_crawler(crawler_name: str, output_dir: str) -> Any:
    """
    Создаёт экземпляр загрузчика изображений по имени источника.

    :param crawler_name: Название источника ('google', 'bing', 'flickr').
    :param output_dir: Папка для сохранения изображений.
    :return: Объект загрузчика icrawler.
    :raises ValueError: если указан неверный источник.
    """
    crawlers = {
        "google": GoogleImageCrawler,
        "bing": BingImageCrawler,
        "flickr": FlickrImageCrawler
    }

    if crawler_name not in crawlers:
        raise ValueError(f"Неверный источник: {crawler_name}")

    return crawlers[crawler_name](storage={'root_dir': output_dir})


def download_images(crawler: Any, num_images: int) -> None:
    """
    Загружает изображения по ключевому слову 'hedgehog'.

    :param crawler: Объект загрузчика icrawler.
    :param num_images: Количество изображений для скачивания.
    :raises RuntimeError: при ошибке загрузки.
    """
    try:
        print(f"Скачивание {num_images} изображений 'hedgehog'...")
        crawler.crawl(keyword="hedgehog", max_num=num_images)
        print("Загрузка завершена успешно.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке изображений: {e}") from e


def main() -> None:
    """
    Главная функция программы.
    """
    args = parse_arguments()

    try:
        validate_num_images(args.num)
        ensure_directory(args.output_dir)

        print(f"Выбран источник: {args.crawler.capitalize()}")
        crawler = create_crawler(args.crawler, args.output_dir)
        download_images(crawler, args.num)

        print(f"Изображения сохранены в: {os.path.abspath(args.output_dir)}")

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except RuntimeError as re:
        print(f"Ошибка выполнения: {re}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
