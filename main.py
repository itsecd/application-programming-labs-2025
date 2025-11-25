import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",
                        help="(google, bing, flickr)")
    parser.add_argument("--storage-dir",
                        help="save folder")
    parser.add_argument("--count", type=int,
                        help="count of images")

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

    crawler.crawl(keyword='hedgehog', max_num=args.count, min_size=(200, 200), max_size=(2000,2000))
    print(f"Images saved to: {args.storage_dir}")

    create_annotation(args.storage_dir)


def create_annotation(storage_dir):
    annotation_file = "annotation.csv"
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

if __name__ == '__main__':
    main()
