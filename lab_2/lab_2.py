import csv
from pathlib import Path
from icrawler.builtin import BingImageCrawler
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Скачивание изображений и создание аннотации")
    parser.add_argument('--images_dir', type=Path, required=True ,help='images_dir например "images" ')
    parser.add_argument('--annotation', type=Path, default=Path("annotation.csv"), help='annotation например "annotation.csv"')
    parser.add_argument('--query', nargs='+', type=str , help='keyword например "машина природа"')
    parser.add_argument('--count', type=int, default=2,help='количество фото')
if __name__ == "__main__":
    main()