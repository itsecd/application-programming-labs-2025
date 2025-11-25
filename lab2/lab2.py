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
    print(f"Folder: {args.folder}")
    print(f"CSV: {args.csv}")
    print(f"Words: {args.words}")
    print(f"Count: {args.count}")


if __name__ == "__main__":
    run()