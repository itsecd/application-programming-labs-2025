import os

from icrawler.builtin import BingImageCrawler


def download_images(dir: str, colors: list[str], count: int) -> None:
    """
    Скачивает изображения черепахи с указанными цветами
    :param dir: путь к папке с изображениями черепахи
    :param colors: список цветов
    :param count: количество изображений
    """
    # Определяем, сколько изображений нужно скачать для каждого цвета
    count_img = count // len(colors)

    print(f"Cкачивание {count} изображений по {count_img} на цвет в {dir}")

    if not os.path.exists(dir):
        os.makedirs(dir)

    for color in colors:
        print(f"Скачивание черепах цвета {color}")

        # Создаем подпапку для каждого цвета
        color_dir = os.path.join(dir, color)
        if not os.path.exists(color_dir):
            os.makedirs(color_dir)

        # Инициализируем краулер
        crawler = BingImageCrawler(feeder_threads=1,
                                   parser_threads=1,
                                   downloader_threads=1,
                                   storage={'root_dir': color_dir})

        crawler.crawl(keyword=f"{color} turtle", max_num=count_img)
