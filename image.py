import csv
import os
import time
from datetime import date

from icrawler.builtin import GoogleImageCrawler


class ImageIterator:
    """Class for iteration by images"""
    def __init__(self, source):
        self.paths = []
        self.counter = 0

        if isinstance(source, str):
            if source.endswith(".csv"):
                with open(source, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.paths.append(row["Absolute Path"])
            else:
                for file in os.listdir(source):
                    if file.endswith((".png", ".jpg", ".jpeg")):
                        self.paths.append(os.path.join(source, file))
        else:
            raise RuntimeError("Cannot create iterable object")

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        """Iteration. Get next element"""
        if self.counter < len(self.paths):
            path = self.paths[self.counter]
            self.counter += 1
            return path
        else:
            raise StopIteration


def parse_date_range(date_range_str: str) -> list[date]:
    """Parse string to list of dates"""
    date_range = list(map(int, date_range_str.split('-')))
    if len(date_range) != 6:
        raise ValueError(f"Invalid date format. Usage: YYYY-MM-DD-YYYY-MM-DD")
    return [date(date_range[0], date_range[1], date_range[2]), date(date_range[3], date_range[4], date_range[5])]


def download_horse_images(start: date, end: date, directory: str, count: int) -> list[str]:
    """Download images with horses in specified dates range"""

    os.makedirs(directory, exist_ok=True)
    keywords = ["хобби хорсер", "hobby horser", "hobbyhorser", "horse", "pony", "horsephoto"]
    downloaded_paths = set()
    if not (os.listdir(directory) is None):
        for file_path in os.listdir(directory):
            if file_path.endswith(('.jpg', '.jpeg', '.png')):
                downloaded_paths.add(file_path)
    i = 0
    while len(downloaded_paths) < count and i < len(keywords):
        try:
            filters = dict(
                type='photo',
                date=(start, end)
            )
            crawler = GoogleImageCrawler(
                storage={'root_dir': directory},
                downloader_threads=4,
                log_level=50
            )

            crawler.crawl(
                keyword=keywords[i],
                filters=filters,
                max_num=count - len(downloaded_paths),
                file_idx_offset=len(downloaded_paths)
            )

            time.sleep(2)
            if not (os.listdir(directory) is None):
                for file_path in os.listdir(directory):
                    if file_path.endswith(('.jpg', '.jpeg', '.png')):
                        downloaded_paths.add(file_path)

            actual_downloaded = len(downloaded_paths)
            print(f"Downloaded {actual_downloaded}/{count}")

            i += 1

        except Exception as e:
            print(f"Something went wrong: {e}")
            i += 1
    return sorted(downloaded_paths)


def create_annotation_csv(image_paths: list[str], annotation_file: str, directory: str) -> None:
    """Generator csv annotation"""
    with open(annotation_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Absolute Path', 'Relative Path'])

        for path in image_paths:
            abs_path = os.path.abspath(os.path.join(directory, path))
            rel_path = os.path.join(directory, path)
            writer.writerow([abs_path, rel_path])

