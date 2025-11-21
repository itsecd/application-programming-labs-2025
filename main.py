import argparse
import os
from download import (
    crawler_initial,
    images_download
)
from file import create_annotation_csv
from iterator import Iterator




def parse_arguments() -> argparse.Namespace:
    """
    parse argumenrs command line
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="images count [50–1000]"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="craw_res",
        required=True,
        help="output dir"
    )
    parser.add_argument(
        "--craw",
        type=str,
        required=True,
        choices=["google", "bing", "flic"],
        help="download source [google, bing, flic]"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="annotation.csv",
        help="csv file name"
    )
    return parser.parse_args()





def main() -> None:
    """main function"""
    args = parse_arguments()


    try:

        crawler = crawler_initial(args.craw, args.output_dir)

        images_download(crawler, args.count)
        create_annotation_csv(args.output_dir, args.csv)

        for path in Iterator(args.csv):
            print("Path: ", path)

        print("finished")



    except Exception as e:
        print(f"something error :(\n {e}")

if __name__ == "__main__":
    main()