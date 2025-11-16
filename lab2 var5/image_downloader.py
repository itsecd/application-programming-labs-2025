from icrawler.builtin import BingImageCrawler
from pathlib import Path


def download_images(keyword: str, color: str, output_dir: Path, max_num: int = 100):
    """
    Скачивает изображения по запросу и цвету.
    :param keyword: Строка поиска (например, "птица").
    :param color: Цвет изображения ('красный', 'желтый' и т.п.).
    :param output_dir: Директория для сохранения изображений.
    :param max_num: Максимальное количество загружаемых изображений.
    """
    bing_crawler = BingImageCrawler(storage={"root_dir": str(output_dir)})
    filters = {"color": color.lower()}  # фильтры цветов могут отличаться для разных сервисов
    bing_crawler.crawl(keyword=keyword, filters=filters, max_num=max_num)