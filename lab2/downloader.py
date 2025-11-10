import os
from typing import Any
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler


def ensure_directory(path: str) -> None:
    """
    Проверяет наличие директории и создаёт её при необходимости.
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
    """
    try:
        print(f"Скачивание {num_images} изображений 'hedgehog'...")
        crawler.crawl(keyword="hedgehog", max_num=num_images)
        print("Загрузка завершена успешно.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке изображений: {e}") from e
