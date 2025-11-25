from icrawler.builtin import BingImageCrawler
import argparse
import os
import csv


def read_arguments():
    parser = argparse.ArgumentParser(
        description="Download multiple horse images by keywords and annotate paths."
    )
    parser.add_argument("--folder", required=True, help="Directory for downloaded images")
    parser.add_argument("--csv", required=True, help="Target CSV file")
    parser.add_argument("--words", nargs="+", required=True, help="List of keywords")
    parser.add_argument("--count", type=int, required=True, help="Images per keyword")
    return parser.parse_args()


def run():
    args = read_arguments()

    crawler = BingImageCrawler(storage={"root_dir": args.folder})

    for keyword in args.words:
        print(f"Downloading images for: {keyword}")
        crawler.crawl(
            keyword=keyword,
            max_num=args.count
        )


if __name__ == "__main__":
    run()