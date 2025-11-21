import argparse
import os



def parse_arguments() -> argparse.Namespace:
    """
    parse argumenrs command line
    """
    parser.add_argument(
        "--craw",
        type=str,
        required=True,
        choices=["google", "bing", "flickr"],
        help="download source [google, bing, flic]"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="craw_res"
        required=True,
        help="output dir"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="images count [50–1000]"
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

if __name__ == "__main__":
    main()