import random
from typing import List, Tuple
from icrawler.builtin import GoogleImageCrawler


class ImageDownloader:

    def __init__(self, keyword: str, storage_dir: str) -> None:
        self.keyword = keyword
        self.storage_dir = storage_dir

    def download_images(self, size_ranges: List[Tuple[int, int]], total_images: int) -> None:
        if total_images < len(size_ranges):
            raise ValueError("Общее количество изображений меньше количества диапазонов!")

        try:
            remaining = total_images
            for i, size_range in enumerate(size_ranges):
                if i == len(size_ranges) - 1:
                    count = remaining
                else:
                    count = random.randint(1, remaining - (len(size_ranges) - i - 1))
                    remaining -= count

                crawler = GoogleImageCrawler(storage={'root_dir': self.storage_dir})
                print(f"Скачиваем {count} изображений размером {size_range}...")
                crawler.crawl(
                    keyword=self.keyword,
                    max_num=count,
                    min_size=size_range[0],
                    max_size=size_range[1]
                )
        except Exception as e:
            print(f"Произошла ошибка при скачивании изображений: {e}")


def get_size_ranges() -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    while True:
        try:
            user_input = input(
                "Введите диапазон размеров через пробел (min max), или 'stop' для окончания: "
            )
            if user_input.lower() == 'stop':
                break

            min_size, max_size = map(int, user_input.split())
            if min_size > max_size:
                print("Минимальный размер не может быть больше максимального!")
                continue

            ranges.append((min_size, max_size))
        except ValueError:
            print("Неправильный ввод. Введите два числа через пробел.")
    return ranges


def main() -> None:
    keyword = "fish"
    storage_dir = "fish_images"
    total_images = random.randint(50, 1000)

    print(f"Будет скачано всего {total_images} изображений по ключевому слову '{keyword}'")

    size_ranges = get_size_ranges()
    if not size_ranges:
        print("Диапазоны размеров не заданы, выходим...")
        return

    downloader = ImageDownloader(keyword, storage_dir)
    downloader.download_images(size_ranges, total_images)


if __name__ == '__main__':
    main()