import argparse
import os
import downloader

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
        help='List of colors to search. Example: red green'
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

    print("Args for script:")
    print(f"    Colors: {args.colors}")
    print(f"    Directory to save images: {args.output_dir}")
    print(f"    Filepath to save CSV table: {args.annotation_path}")
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Directory {args.output_dir} created!")

    #code
    downloaded_paths = downloader.download_images(
        key="snake",
        colors=args.colors,
        root_dir=args.output_dir
    )

    if (downloaded_paths):
        print(f"Downloaded {len(downloaded_paths)} files.")
    else:
        print(f"Won't able to download any images!")

if __name__ == "__main__":
    main()