import os
import random
from icrawler.builtin import BingImageCrawler


def _calculate_count(colors: list[str], min_val: int, max_val: int) -> dict[str, int]:
    """
    Ensures that we have at least 1 image per color, and total number of images in set range.

    :param colors: List of colors to download.
    :param min_val: Minimum value of required downloaded pictures.
    :param max_val: Maximum value of required downloaded pictures.
    :return: Dictionary of how many images need to download per color.
    """
    num_colors = len(colors)

    if min_val < num_colors:
        min_val = num_colors

    total_images = random.randint(min_val, max_val)

    count = {color: 1 for color in colors}
    remain_to_count = total_images - num_colors

    for _ in range(remain_to_count):
        color_to_add = random.choice(colors)
        count[color_to_add] += 1

    return count


def download_images(key: str, colors: list[str], root_dir: str) -> list[str]:
    """
    Download images by keyword with color variations.

    :param key: Keyword for search.
    :param colors: List of colors to search with keyword.
    :param root_dir: Root directory to save files.
    :return: List of absolute paths to all images.
    """
    all_images_path = []
    print("Downloading...")

    image_count = _calculate_count(colors, 50, 1000)

    for color, num_images in image_count.items():
        search_key = color + " " + key
        print(f"search_key: {search_key}")
        color_dir = os.path.join(root_dir, color)

        print(f"Searching: {search_key} in quantity: {num_images}, saving to: {color_dir}")

        google_crawler = BingImageCrawler(storage={'root_dir': color_dir})
        google_crawler.crawl(keyword=search_key, max_num=num_images)

        # take paths
        try:
            downloaded_files = os.listdir(color_dir)
            for file in downloaded_files:
                full_path = os.path.abspath(os.path.join(color_dir, file))
                if os.path.isfile(full_path):
                    all_images_path.append(full_path)
        except FileNotFoundError:
            print(f"Can't find directory for downloaded images! Maybe no files were downloaded?")

    return all_images_path
