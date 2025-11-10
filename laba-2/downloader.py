import os
import random
from icrawler.builtin import GoogleImageCrawler

def download_images(key: str, colors: list[str], root_dir: str) -> list[str]:
    """
    Download images by keyword with color variations.

    :param key: Keyword for search
    :paramm colors: List of colors to search with keyword
    :param root_dir: Root directory to save files
    :return: List of absolute paths to all images
    """
    all_images_path = []
    print("Downloading...")

    for color in colors:
        search_key = color + " " + key
        print(f"search_key: {search_key}")
        color_dir = os.path.join(root_dir, color)

        #TODO add check at last that we created at least 50 in total
        number_of_images = random.randint(1, 100)

        print(f"Searching: {search_key} in quantity: {number_of_images}, saving to: {color_dir}")

        google_crawler = GoogleImageCrawler(storage={'root_dir': color_dir})
        google_crawler.crawl(keyword=search_key, max_num=number_of_images)

        #take paths
        try:
            downloaded_files = os.listdir(color_dir)
            for file in downloaded_files:
                all_images_path.append(os.path.abspath(os.path.join(color_dir, file)))
        except FileNotFoundError:
            print(f"Can't find directory for downloaded images! Maybe no files were downloaded?")

    return all_images_path