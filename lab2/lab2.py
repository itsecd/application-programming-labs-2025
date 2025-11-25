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


def generate_csv(csv_path, base_folder):
    root_origin = os.path.dirname(os.path.abspath(csv_path))

    rows = []
    for root, _, files in os.walk(base_folder):
        for name in files:
            abs_p = os.path.abspath(os.path.join(root, name))
            rel_p = os.path.relpath(abs_p, start=root_origin)
            rows.append((abs_p, rel_p))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["absolute_path", "relative_path"])
        writer.writerows(rows)


def run():
    args = read_arguments()

    crawler = BingImageCrawler(storage={"root_dir": args.folder})

    for keyword in args.words:
        print(f"Downloading images for: {keyword}")
        crawler.crawl(
            keyword=keyword,
            max_num=args.count
        )

    generate_csv(args.csv, args.folder)


if __name__ == "__main__":
    run()