import argparse
import os

def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments
    """
    parser = argparse.ArgumentParser(description="Web scraper for dowbloading snake images by color.")
    parser.add_argument(
        '--colors',
        '-c',
        required=True,
        nargs='+',
        help='List of colors to search.'
    )
    parser.add_argument(
        '--output_dir',
        '-o',
        default='dataset',
        help='Directory to store saved images.'
    )
    parser.add_argument(
        '--annotation_path',
        '-a',
        default='annotation.csv',
        help='Filepath to save CSV annotation.'
    )
    return parser.parse_args()

def main():
    """
    Main function
    """
    args = parse_arguments()

    print("Run a script")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Directory {atgs.output_dir} created!")

    #code

if __name__ == "__main__":
    main()