import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler, BaiduImageCrawler
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",
                        help="(google, bing, flickr, baidu)")
    parser.add_argument("--storage-dir",
                        help="save folder")
    parser.add_argument("--count", type=int,
                        help="count of images")
    parser.add_argument("--annotation-file",
                        help="path for CSV annotation")

    args = parser.parse_args()


    if args.count < 50 or args.count > 1000:
        print("Error: count must be greater than 50 and less than 100.")
        return

    if args.source == 'google':
        crawler = GoogleImageCrawler(storage={'root_dir': args.storage_dir})
    elif args.source == 'bing':
        crawler = BingImageCrawler(storage={'root_dir': args.storage_dir})
    elif args.source == 'flickr':
        crawler = FlickrImageCrawler(storage={'root_dir': args.storage_dir})
    elif args.source == 'baidu':
        crawler = BaiduImageCrawler(storage={'root_dir': args.storage_dir})

    crawler.crawl(keyword='hedgehog', max_num=args.count, min_size=(200, 200), max_size=(2000,2000))
    print(f"Images saved to: {args.storage_dir}")

    create_annotation(args.storage_dir, args.annotation_file)


def create_annotation(storage_dir, annotation_file):
    storage_path = Path(storage_dir)
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(storage_path.rglob(ext))
    if not image_files:
        print("No images found for annotation")
        return


    with open(annotation_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for img_path in image_files:
            abs_path = str(img_path.absolute())
            rel_path = str(img_path.relative_to(storage_path))
            writer.writerow([abs_path, rel_path])


class ImagePathIterator:

    def __init__(self, annotation_file=None, folder_path=None):
        self.paths = []
        self.index = 0

        if annotation_file:
            self._load_from_csv(annotation_file)
        elif folder_path:
            self._load_from_folder(folder_path)

    def _load_from_csv(self, annotation_file):
        with open(annotation_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    self.paths.append(row[0])

    def _load_from_folder(self, folder_path):
        folder = Path(folder_path)
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            for img_path in folder.rglob(ext):
                self.paths.append(str(img_path.absolute()))

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration

if __name__ == '__main__':
    main()
